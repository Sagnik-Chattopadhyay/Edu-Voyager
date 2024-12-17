import csv
from django.core.management.base import BaseCommand
from user.models import College

class Command(BaseCommand):
    help = "Import college data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', type=str, help="Path to the CSV file containing college data"
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                # Validate CSV headers
                expected_headers = {'name', 'country', 'ranking', 'tuition_fee', 'programs', 'scholarships', 'link'}
                if not expected_headers.issubset(reader.fieldnames):
                    missing_headers = expected_headers - set(reader.fieldnames)
                    self.stdout.write(self.style.ERROR(f"Missing required headers: {', '.join(missing_headers)}"))
                    return

                # Import rows
                for row in reader:
                    try:
                        College.objects.update_or_create(
                            name=row['name'],  # Ensure uniqueness based on name
                            defaults={
                                'country': row['country'],
                                'ranking': int(row['ranking']) if row['ranking'] else None,
                                'tuition_fee': float(row['tuition_fee']) if row['tuition_fee'] else None,
                                'programs': row['programs'],
                                'scholarships': row['scholarships'].strip().lower() == 'true',
                                'link': row['link'] if row['link'] else None,
                            }
                        )
                        self.stdout.write(self.style.SUCCESS(f"Imported: {row['name']}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error importing row {row['name']}: {e}"))

            self.stdout.write(self.style.SUCCESS("College data imported successfully!"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file_path}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing data: {e}"))
