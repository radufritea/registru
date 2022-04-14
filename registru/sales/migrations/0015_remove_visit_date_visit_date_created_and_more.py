# Generated by Django 4.0.2 on 2022-03-02 14:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0014_visit_products_delete_presence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='date',
        ),
        migrations.AddField(
            model_name='visit',
            name='date_created',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='visit',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
