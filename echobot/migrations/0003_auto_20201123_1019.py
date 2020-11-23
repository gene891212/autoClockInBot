# Generated by Django 3.1.2 on 2020-11-23 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('echobot', '0002_userinformation_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinformation',
            name='user_id',
            field=models.CharField(help_text='It will auto fill from linbot.', max_length=200),
        ),
        migrations.AlterField(
            model_name='userinformation',
            name='user_name',
            field=models.CharField(blank=True, help_text='It will auto fill from linbot.', max_length=200),
        ),
    ]
