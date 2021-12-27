# Generated by Django 3.2.9 on 2021-12-26 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_managing', '0003_auto_20211226_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='status',
            field=models.CharField(choices=[('pen', 'Pending'), ('del', 'Deleted'), ('con', 'Confirmed')], default='pen', max_length=3),
        ),
        migrations.AlterField(
            model_name='shoptype',
            name='status',
            field=models.CharField(choices=[('dru', 'drugstore'), ('boo', 'bookshop'), ('swe', 'sweetshop'), ('dai', 'dairy')], max_length=3),
        ),
    ]
