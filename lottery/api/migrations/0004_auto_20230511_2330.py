# Generated by Django 3.2 on 2023-05-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_lotterytype_number_of_digits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='winningtype',
            name='number_of_digits',
        ),
        migrations.AlterField(
            model_name='order',
            name='winning_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
