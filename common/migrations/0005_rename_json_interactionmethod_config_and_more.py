# Generated by Django 4.0.5 on 2023-06-13 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_interactionmethod_delete_technicalmetadata_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interactionmethod',
            old_name='json',
            new_name='config',
        ),
        migrations.RenameField(
            model_name='interactionmethod',
            old_name='interaction_method',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='scientificmetadata',
            old_name='resource_type',
            new_name='type',
        ),
    ]