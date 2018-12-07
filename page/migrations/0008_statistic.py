# Generated by Django 2.1.2 on 2018-10-07 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0007_delete_statistics'),
    ]

    operations = [
        migrations.CreateModel(
            name='statistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('header', models.CharField(max_length=360)),
                ('allow', models.CharField(max_length=360)),
                ('end', models.DateTimeField()),
            ],
        ),
    ]