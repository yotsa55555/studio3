# Generated by Django 5.1.1 on 2024-10-14 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_borrowing_borrowed_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowing',
            old_name='equipment_id',
            new_name='equipment',
        ),
    ]
