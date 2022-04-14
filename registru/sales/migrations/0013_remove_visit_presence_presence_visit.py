# Generated by Django 4.0.2 on 2022-03-01 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0012_presence_delete_showpresence_visit_presence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='presence',
        ),
        migrations.AddField(
            model_name='presence',
            name='visit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.visit'),
        ),
    ]
