# Generated by Django 5.1.4 on 2024-12-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capitals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='capital',
            name='is_primary',
            field=models.BooleanField(default=False),
        ),
    ]
