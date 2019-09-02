# Generated by Django 2.2.4 on 2019-09-02 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_places', '0002_auto_20190901_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='price_level',
            field=models.SmallIntegerField(choices=[(0, 'Free'), (1, 'Inexpensive'), (2, 'Moderate'), (3, 'Expensive'), (4, 'Very Expensive'), (5, 'Unknown price')], default=5),
        ),
    ]