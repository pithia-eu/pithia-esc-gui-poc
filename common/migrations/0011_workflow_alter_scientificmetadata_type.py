# Generated by Django 4.0.5 on 2024-01-15 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_scientificmetadata_institution_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workflow',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('common.scientificmetadata',),
        ),
        migrations.AlterField(
            model_name='scientificmetadata',
            name='type',
            field=models.CharField(choices=[('organisation', 'Organisation'), ('individual', 'Individual'), ('project', 'Project'), ('platform', 'Platform'), ('operation', 'Operation'), ('instrument', 'Instrument'), ('acquisition_capabilities', 'Acquisition Capabilities'), ('acquisition', 'Acquisition'), ('computation_capabilities', 'Computation Capabilities'), ('computation', 'Computation'), ('process', 'Process'), ('data_collection', 'Data Collection'), ('catalogue', 'Catalogue'), ('catalogue_entry', 'Catalogue Entry'), ('catalogue_data_subset', 'Catalogue Data Subset'), ('workflow', 'Workflow')], db_column='sm_type', max_length=100),
        ),
    ]
