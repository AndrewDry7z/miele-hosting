# Generated by Django 2.2 on 2020-07-28 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_catalog_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='catalog_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='api.Catalog'),
        ),
    ]
