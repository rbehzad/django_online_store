# Generated by Django 3.2.9 on 2022-01-12 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_managing', '0008_alter_shop_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Deleted', 'Deleted'), ('Pending', 'Pending')], default='Pending', max_length=12),
        ),
    ]
