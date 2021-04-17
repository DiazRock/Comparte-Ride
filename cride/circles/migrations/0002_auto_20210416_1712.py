# Generated by Django 2.0.9 on 2021-04-16 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='circle',
            options={'get_latest_by': 'created', 'ordering': ['-rides_taken', '-rides_offerted']},
        ),
        migrations.RenameField(
            model_name='circle',
            old_name='rides_offered',
            new_name='rides_offerted',
        ),
    ]
