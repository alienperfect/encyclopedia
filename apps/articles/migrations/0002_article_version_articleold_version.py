# Generated by Django 4.0 on 2022-01-12 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='version',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='articleold',
            name='version',
            field=models.IntegerField(default=1),
        ),
    ]
