# Generated by Django 2.2.4 on 2019-09-01 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_places', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='formatted_address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='places',
            name='name',
            field=models.TextField(),
        ),
    ]
