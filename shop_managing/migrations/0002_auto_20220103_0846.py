# Generated by Django 3.2.9 on 2022-01-03 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_managing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(to='shop_managing.Tag'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Deleted', 'Deleted')], default='Pending', max_length=12),
        ),
    ]