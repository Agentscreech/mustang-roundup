# Generated by Django 2.0.3 on 2018-03-11 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mustangroundup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='peoples_choice',
            name='category',
            field=models.CharField(default='default', max_length=200),
            preserve_default=False,
        ),
    ]
