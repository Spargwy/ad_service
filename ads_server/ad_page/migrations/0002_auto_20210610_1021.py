# Generated by Django 3.2.4 on 2021-06-10 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_page', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ad',
            options={'ordering': ('-created',)},
        ),
        migrations.RemoveField(
            model_name='ad',
            name='top',
        ),
        migrations.AddField(
            model_name='ad',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]