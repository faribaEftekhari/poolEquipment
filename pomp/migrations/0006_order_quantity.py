# Generated by Django 3.2.5 on 2021-08-20 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pomp', '0005_auto_20210820_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
