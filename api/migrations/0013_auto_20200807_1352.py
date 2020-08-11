# Generated by Django 2.2 on 2020-08-07 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200806_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='country',
            field=models.ForeignKey(blank=True, default=None, on_delete=models.SET('DELETED'), to='api.Countries'),
        ),
        migrations.AlterField(
            model_name='person',
            name='photo',
            field=models.FileField(blank=True, default=None, upload_to='media/users/'),
        ),
    ]