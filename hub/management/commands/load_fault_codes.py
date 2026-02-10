from django.core.management.base import BaseCommand
import openpyxl
from hub.models import VFDModel, ErrorCode

class Command(BaseCommand):
    help = 'Load fault codes from Veichi Fault Codes.xlsx'

    def handle(self, *args, **options):
        file_path = 'Veichi Fault Codes.xlsx'
        try:
            wb = openpyxl.load_workbook(file_path)
            ws = wb.active
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{file_path}" not found.'))
            return

        # Get or create the generic VFD Model
        vfd_model, created = VFDModel.objects.get_or_create(
            series_name="Veichi General",
            defaults={'power_rating': 'All', 'description': 'Generic codes for Veichi devices'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created VFDModel: {vfd_model}'))
        else:
            self.stdout.write(f'Using existing VFDModel: {vfd_model}')

        # Headers are: Code, Type, Description / Alarm Type, Possible Cause, Troubleshooting
        # Row iterator starts at 2 to skip headers
        count = 0
        for row in ws.iter_rows(min_row=2, values_only=True):
            code_val = row[0]
            if not code_val:
                continue
                
            type_val = row[1] or ''
            desc_val = row[2] or '' # Description / Alarm Type
            cause_val = row[3] or '' # Possible Cause
            trouble_val = row[4] or '' # Troubleshooting

            # Mapping
            # code -> code
            # name -> Description / Alarm Type
            # description -> Possible Cause (+ Type if useful, but maybe just Cause)
            # troubleshooting_steps -> Troubleshooting

            error_code, created = ErrorCode.objects.update_or_create(
                vfd_model=vfd_model,
                code=str(code_val).strip(),
                defaults={
                    'name': str(desc_val).strip(),
                    'description': str(cause_val).strip(),
                    'troubleshooting_steps': str(trouble_val).strip(),
                }
            )
            count += 1
            action = "Created" if created else "Updated"
            # self.stdout.write(f'{action} code {error_code.code}')

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {count} fault codes.'))
