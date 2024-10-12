# Generated by Django 5.1.1 on 2024-10-09 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_equipment_unique_parcel_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='equipment',
            name='image',
            field=models.ImageField(default='media/images/default.jpg', upload_to='images/'),
        ),
    ]