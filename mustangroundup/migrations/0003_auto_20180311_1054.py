# Generated by Django 2.0.3 on 2018-03-11 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mustangroundup', '0002_peoples_choice_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='peoples_choice',
            old_name='category_entry',
            new_name='car_id',
        ),
        migrations.RemoveField(
            model_name='peoples_choice',
            name='category',
        ),
    ]
