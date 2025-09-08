from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_alter_reservationlot_soft_delete'),
    ]

    operations = [
        # Raw SQL to drop the NOT NULL constraint on PostgreSQL
        migrations.RunSQL(
            # Forward: Make column nullable
            "ALTER TABLE reservation_reservationlot ALTER COLUMN soft_delete DROP NOT NULL;",
            # Reverse: Make column not nullable again
            "ALTER TABLE reservation_reservationlot ALTER COLUMN soft_delete SET NOT NULL;",
        ),
    ]