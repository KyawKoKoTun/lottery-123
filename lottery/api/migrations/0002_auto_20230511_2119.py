# Generated by Django 3.2 on 2023-05-11 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='winningtype',
            name='label',
        ),
        migrations.RemoveField(
            model_name='winningtype',
            name='limit_amount',
        ),
        migrations.RemoveField(
            model_name='winningtype',
            name='overflow_amount',
        ),
        migrations.RemoveField(
            model_name='winningtype',
            name='single_user_win',
        ),
        migrations.RemoveField(
            model_name='winningtype',
            name='weekly_increment_amount',
        ),
    ]