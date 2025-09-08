from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservationlot',
            name='soft_delete',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]