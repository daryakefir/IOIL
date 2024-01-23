# Generated by Django 4.1 on 2024-01-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FallRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.PositiveIntegerField()),
                ('first_m', models.FloatField()),
                ('second_m', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='WaterCutCatalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water_cut_value', models.FloatField()),
                ('first_characteristic', models.FloatField()),
                ('second_characteristic', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Well',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('liquid_yield', models.FloatField()),
                ('oil_yield', models.FloatField()),
                ('oil_produced', models.FloatField()),
                ('oil_reserve', models.FloatField()),
                ('water_cut', models.FloatField()),
            ],
        ),
    ]
