from django.core.management.base import BaseCommand
from parking.models import ParkingLot, ParkingSpace


class Command(BaseCommand):
    help = 'Create parking lots and spaces for the application'

    def handle(self, *args, **options):
        # Create a parking lot first
        lot, created = ParkingLot.objects.get_or_create(
            name='Main Parking Lot',
            defaults={
                'location': '123 Main St, Downtown',
                'total_spaces': 20
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created parking lot: {lot.name}')
            )
        else:
            self.stdout.write(f'Parking lot already exists: {lot.name}')

        # Create parking spaces
        spaces_created = 0
        for i in range(1, 21):  # Create 20 spaces
            space, created = ParkingSpace.objects.get_or_create(
                lot=lot,
                label=f'A{i:02d}',
                defaults={
                    'is_occupied': False,
                    'is_reserved': False,
                    'sensor_id': f'sensor_{i}'
                }
            )
            if created:
                spaces_created += 1

        if spaces_created > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Created {spaces_created} new parking spaces')
            )
        
        total_spaces = ParkingSpace.objects.count()
        self.stdout.write(f'Total parking spaces in database: {total_spaces}')