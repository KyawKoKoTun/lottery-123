# Generated by Django 3.2 on 2023-05-11 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20230511_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotterytype',
            name='number_of_digits',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
