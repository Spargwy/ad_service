# Generated by Django 3.2.4 on 2021-06-10 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('price', models.IntegerField()),
                ('hot_price', models.IntegerField(null=True)),
                ('top', models.BooleanField(null=True)),
            ],
        ),
    ]