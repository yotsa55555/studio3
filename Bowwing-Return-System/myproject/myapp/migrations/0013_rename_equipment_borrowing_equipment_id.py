# Generated by Django 5.1.1 on 2024-10-14 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_alter_student_kkumail_alter_student_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowing',
            old_name='equipment',
            new_name='equipment_id',
        ),
    ]