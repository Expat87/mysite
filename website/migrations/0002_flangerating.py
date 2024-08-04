# Generated by Django 3.2.25 on 2024-07-27 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlangeRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.FloatField()),
                ('flange_rating', models.FloatField()),
                ('max_p', models.FloatField()),
                ('temp_range', models.FloatField()),
            ],
        ),
    ]
