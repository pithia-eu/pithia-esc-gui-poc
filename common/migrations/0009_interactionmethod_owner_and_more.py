# Generated by Django 4.0.5 on 2023-10-02 14:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_interactionmethod_deactivated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='interactionmethod',
            name='owner',
            field=models.CharField(db_column='owner_id', default=django.utils.timezone.now, max_length=9999),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='handleurlmapping',
            name='handle_name',
            field=models.CharField(db_column='doi_name', max_length=100),
        ),
        migrations.AlterField(
            model_name='handleurlmapping',
            name='id',
            field=models.CharField(db_column='doi_id', max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='handleurlmapping',
            name='url',
            field=models.URLField(db_column='doi_url'),
        ),
        migrations.AlterField(
            model_name='interactionmethod',
            name='config',
            field=models.JSONField(db_column='intm_config'),
        ),
        migrations.AlterField(
            model_name='interactionmethod',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='intm_reg_date'),
        ),
        migrations.AlterField(
            model_name='interactionmethod',
            name='data_collection',
            field=models.ForeignKey(db_column='sm_id', limit_choices_to={'type': 'data_collection'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.datacollection'),
        ),
        migrations.AlterField(
            model_name='interactionmethod',
            name='deactivated',
            field=models.BooleanField(db_column='intm_deactivated', default=False),
        ),
        migrations.AlterField(
            model_name='interactionmethod',
            name='id',
            field=models.CharField(db_column='intm_id', max_length=36, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='interactionmethod',
            name='type',
            field=models.CharField(choices=[('api', 'API')], db_column='intm_type', default='api', max_length=100),
        ),
        migrations.AlterField(
            model_name='interactionmethod',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_column='intm_upd_date'),
        ),
        migrations.AlterField(
            model_name='scientificmetadata',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='sm_reg_date'),
        ),
        migrations.AlterField(
            model_name='scientificmetadata',
            name='deactivated',
            field=models.BooleanField(db_column='sm_deactivated', default=False),
        ),
        migrations.AlterField(
            model_name='scientificmetadata',
            name='id',
            field=models.CharField(db_column='sm_id', max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='scientificmetadata',
            name='json',
            field=models.JSONField(db_column='sm_json_support'),
        ),
        migrations.AlterField(
            model_name='scientificmetadata',
            name='type',
            field=models.CharField(choices=[('organisation', 'Organisation'), ('individual', 'Individual'), ('project', 'Project'), ('platform', 'Platform'), ('operation', 'Operation'), ('instrument', 'Instrument'), ('acquisition_capabilities', 'Acquisition Capabilities'), ('acquisition', 'Acquisition'), ('computation_capabilities', 'Computation Capabilities'), ('computation', 'Computation'), ('process', 'Process'), ('data_collection', 'Data Collection'), ('catalogue', 'Catalogue'), ('catalogue_entry', 'Catalogue Entry'), ('catalogue_data_subset', 'Catalogue Data Subset')], db_column='sm_type', max_length=100),
        ),
        migrations.AlterField(
            model_name='scientificmetadata',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, db_column='sm_upd_date'),
        ),
        migrations.AlterField(
            model_name='scientificmetadata',
            name='xml',
            field=models.TextField(db_column='sm_metadata_file'),
        ),
        migrations.AlterModelTable(
            name='handleurlmapping',
            table='doi',
        ),
        migrations.AlterModelTable(
            name='interactionmethod',
            table='int_method',
        ),
        migrations.AlterModelTable(
            name='scientificmetadata',
            table='scien_metadata',
        ),
    ]
