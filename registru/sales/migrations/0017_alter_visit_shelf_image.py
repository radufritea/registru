# Generated by Django 4.0.2 on 2022-03-04 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0016_visit_shelf_image_alter_visit_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='shelf_image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]
