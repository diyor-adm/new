# Generated by Django 4.0 on 2021-12-20 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('region', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=256)),
                ('phone_number', models.CharField(max_length=64)),
                ('appeal', models.TextField()),
                ('date_time', models.TextField(max_length=64)),
                ('user_id', models.PositiveIntegerField()),
            ],
        ),
    ]
