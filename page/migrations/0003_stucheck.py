# Generated by Django 2.1.1 on 2018-10-05 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_auto_20181004_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='StuCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stuID', models.CharField(max_length=13)),
                ('phone', models.CharField(max_length=13)),
            ],
        ),
    ]
