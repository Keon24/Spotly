# Generated by Django 5.1.1 on 2025-05-21 00:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('total_spaces', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ParkingSpace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('is_occupied', models.BooleanField(default=False)),
                ('is_reserved', models.BooleanField(default=False)),
                ('sensor_id', models.CharField(max_length=100)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spaces', to='parking.parkinglot')),
            ],
        ),
    ]
