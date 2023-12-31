# Generated by Django 4.2.2 on 2023-06-15 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_section', '0003_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Departure_time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_id', models.IntegerField(primary_key=True, serialize=False)),
                ('departure_city', models.CharField(max_length=80)),
                ('destination_city', models.CharField(max_length=80)),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('traveler_name', models.CharField(max_length=200)),
                ('child_number', models.IntegerField(default=0)),
                ('adult_number', models.IntegerField(default=0)),
                ('phone_number', models.CharField(max_length=15)),
                ('chosen_class', models.CharField(max_length=50)),
                ('seat_number_list', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrainSeat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_number', models.IntegerField(unique=True)),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wagon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wagon', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.TimeField()),
                ('arrival_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals_fee', to='login_section.city')),
                ('departure_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures_fee', to='login_section.city')),
            ],
        ),
        migrations.CreateModel(
            name='Itineraries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult_fee', models.IntegerField()),
                ('child_fee', models.IntegerField()),
                ('duration', models.CharField(max_length=6)),
                ('arrival_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='login_section.city')),
                ('departure_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='login_section.city')),
            ],
        ),
    ]
