# Generated by Django 4.0.2 on 2022-03-07 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0019_alter_visit_shelf_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='date_created',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='WeekPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_num', models.IntegerField()),
                ('date_created', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('monday_goal', models.TextField(blank=True)),
                ('monday_achieved', models.TextField(blank=True)),
                ('tuesday_goal', models.TextField(blank=True)),
                ('tuesday_achieved', models.TextField(blank=True)),
                ('wendsday_goal', models.TextField(blank=True)),
                ('wendsday_achieved', models.TextField(blank=True)),
                ('thursday_goal', models.TextField(blank=True)),
                ('thursday_achieved', models.TextField(blank=True)),
                ('friday_goal', models.TextField(blank=True)),
                ('friday_achieved', models.TextField(blank=True)),
                ('friday_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='friday_location', to='sales.county')),
                ('monday_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monday_location', to='sales.county')),
                ('thursday_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thursday_location', to='sales.county')),
                ('tuesday_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tuesday_location', to='sales.county')),
                ('wendsday_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wendsday_location', to='sales.county')),
            ],
        ),
    ]
