# Generated by Django 4.2 on 2023-04-19 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_connection_device1_alter_connection_device2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='device1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='connections1', to='main.device'),
        ),
    ]
