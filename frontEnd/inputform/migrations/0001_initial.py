# Generated by Django 2.2.6 on 2019-11-01 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=40)),
                ('file', models.FileField(upload_to='')),
                ('quarter', models.CharField(max_length=1)),
                ('students_ids', models.IntegerField(max_length=100)),
                ('students_names', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=40)),
                ('year', models.IntegerField(max_length=4)),
            ],
        ),
    ]
