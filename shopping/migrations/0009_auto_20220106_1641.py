# Generated by Django 3.2.9 on 2022-01-06 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0008_alter_cart_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='title',
            field=models.CharField(default='cart1', max_length=120),
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.CharField(choices=[('Deleted', 'Deleted'), ('Paid', 'Paid'), ('Pending', 'Pending'), ('Confirmed', 'Confirmed')], default='pending', max_length=12),
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('title', 'slug')},
        ),
    ]