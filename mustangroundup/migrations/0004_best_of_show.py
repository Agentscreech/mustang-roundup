# Generated by Django 2.0.3 on 2018-03-11 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mustangroundup', '0003_auto_20180311_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Best_of_show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votes', models.IntegerField(default=0)),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mustangroundup.Car')),
            ],
        ),
    ]
