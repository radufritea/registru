# Generated by Django 4.0.2 on 2022-03-01 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0013_remove_visit_presence_presence_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='products',
            field=models.ManyToManyField(to='sales.Product'),
        ),
        migrations.DeleteModel(
            name='Presence',
        ),
    ]
