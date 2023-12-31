# Generated by Django 3.2.12 on 2023-08-02 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CurrentTime', models.DateTimeField()),
                ('Temperature', models.FloatField()),
                ('Heartbeat', models.IntegerField()),
                ('SpO2', models.IntegerField()),
                ('RBC', models.IntegerField()),
                ('WBC', models.IntegerField()),
                ('Platelets', models.IntegerField()),
                ('BloodGlucose', models.IntegerField()),
                ('HbConcentration', models.IntegerField()),
                ('RespirationRate', models.IntegerField()),
                ('SleepMonitoring', models.IntegerField()),
                ('StepCount', models.IntegerField()),
                ('MovementData', models.IntegerField()),
            ],
        ),
    ]
