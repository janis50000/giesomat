# Generated by Django 3.2.12 on 2022-03-24 15:30

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_name', models.CharField(help_text='Name of the plant.', max_length=200)),
                ('water_need', models.DecimalField(decimal_places=2, default=100, help_text='How much water does the plant need each time it is watered?', max_digits=9)),
                ('is_active', models.BooleanField(default=True, help_text='Is this plant active?')),
                ('current_status', django_fsm.FSMIntegerField(choices=[(0, 'Plant is happy.'), (1, 'Plant is thirsty.'), (2, 'Plant has been watered.')], default=0, help_text='The current status of the plant - this field is set automatically', protected=True)),
                ('water_mode', models.SmallIntegerField(choices=[(0, 'Water plant based on a fixed schedule.'), (1, 'Water plant based on the measured humidity.')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Pump',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpio_pin', models.IntegerField(help_text='Raspberry Pi GPIO Pin of the pump.')),
                ('water_flow_per_minute', models.IntegerField(help_text='Calibration parameter: The water flow through the pump per minute in milli liter')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpio_pin', models.IntegerField(help_text='Raspberry Pi GPIO Pin of the sensor.')),
                ('max_sensor_value', models.IntegerField(help_text='Calibration parameter: Maximum value that the sensor returns when it is in water.')),
                ('min_sensor_value', models.IntegerField(help_text='Calibration parameter: Minimum value that the sensor returns when it is completely dry.')),
                ('sensor_threshold', models.IntegerField(help_text='Threshold of watering the plant. In percentage of minimum / maximum sensor value')),
            ],
        ),
        migrations.CreateModel(
            name='Valve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpio_pin', models.IntegerField(help_text='Raspberry Pi GPIO Pin of the valve.')),
                ('time_offset', models.IntegerField(default=0, help_text='Optional calibration parameter: The time it takes from starting the pump until the water reaches the plant.')),
            ],
        ),
        migrations.CreateModel(
            name='PlantTechnical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='giesomat_app.plant')),
                ('pump', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='giesomat_app.pump')),
                ('sensor', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='giesomat_app.sensor')),
                ('valve', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='giesomat_app.valve')),
            ],
        ),
    ]
