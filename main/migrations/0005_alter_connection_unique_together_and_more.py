# Generated by Django 4.2 on 2023-04-19 04:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_connection_device1_connection_device2_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='connection',
            unique_together={('interface1', 'interface2')},
        ),
        migrations.RemoveField(
            model_name='connection',
            name='device1',
        ),
        migrations.RemoveField(
            model_name='connection',
            name='device2',
        ),
    ]
