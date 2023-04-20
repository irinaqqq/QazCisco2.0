# Generated by Django 4.2 on 2023-04-19 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_connection_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='connection',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='connection',
            name='device1',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='connections1', to='main.device'),
        ),
        migrations.AddField(
            model_name='connection',
            name='device2',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='connections2', to='main.device'),
        ),
        migrations.AlterUniqueTogether(
            name='connection',
            unique_together={('device1', 'interface1', 'device2', 'interface2')},
        ),
    ]