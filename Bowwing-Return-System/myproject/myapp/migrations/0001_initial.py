# Generated by Django 5.1.1 on 2024-10-09 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('kkumail', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=17)),
                ('password', models.CharField(max_length=20)),
                ('student_id_edu', models.CharField(max_length=10)),
                ('major', models.CharField(max_length=100)),
            ],
        ),
    ]