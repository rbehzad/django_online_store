# Generated by Django 3.2.9 on 2022-01-21 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0006_auto_20220120_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('Confirmed', 'Confirmed'), ('Pending', 'Pending'), ('Paid', 'Paid'), ('Canceled', 'Canceled')], default='Pending', max_length=12),
        ),
    ]
