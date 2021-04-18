# Generated by Django 2.0.10 on 2021-04-18 02:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('circles', '0004_auto_20210417_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created at')),
                ('modified', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='modified at')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('used', models.BooleanField(default=False)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circles.Circle')),
                ('issued_by', models.ForeignKey(help_text='Circle member that is providing the invitation', on_delete=django.db.models.deletion.CASCADE, related_name='issued_by', to=settings.AUTH_USER_MODEL)),
                ('used_by', models.ForeignKey(help_text='User that used the code to enter the circle', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
