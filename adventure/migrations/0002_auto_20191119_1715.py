# Generated by Django 2.2.7 on 2019-11-19 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='x_coord',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='y_coord',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]
