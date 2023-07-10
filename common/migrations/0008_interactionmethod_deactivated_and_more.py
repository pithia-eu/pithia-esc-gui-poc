# Generated by Django 4.0.5 on 2023-06-15 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_apiinteractionmethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='interactionmethod',
            name='deactivated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='scientificmetadata',
            name='deactivated',
            field=models.BooleanField(default=False),
        ),
    ]