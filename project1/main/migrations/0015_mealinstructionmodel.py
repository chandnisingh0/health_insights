# Generated by Django 3.1.5 on 2024-02-05 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20240205_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealInstructionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required_meal_age', models.CharField(max_length=50)),
                ('meal_instructions', models.TextField()),
            ],
        ),
    ]
