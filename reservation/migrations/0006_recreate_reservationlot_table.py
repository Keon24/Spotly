from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_merge_20250908_0444'),
        ('parking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Create new table with correct constraints
        migrations.CreateModel(
            name='ReservationLotNew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_code', models.CharField(blank=True, max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reserve_date', models.DateTimeField()),
                ('soft_delete', models.DateTimeField(blank=True, null=True)),
                ('is_occupied', models.BooleanField(default=False)),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.parkingspace')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        # Copy data from old table to new table
        migrations.RunSQL(
            "INSERT INTO reservation_reservationlotnew (id, ticket_code, created_at, reserve_date, soft_delete, is_occupied, space_id, user_id) SELECT id, ticket_code, created_at, reserve_date, soft_delete, is_occupied, space_id, user_id FROM reservation_reservationlot;",
            reverse_sql="DELETE FROM reservation_reservationlotnew;"
        ),
        # Drop old table
        migrations.DeleteModel(
            name='ReservationLot',
        ),
        # Rename new table
        migrations.RenameModel(
            old_name='ReservationLotNew',
            new_name='ReservationLot',
        ),
    ]