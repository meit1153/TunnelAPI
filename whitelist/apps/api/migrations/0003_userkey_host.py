# Generated by Django 2.2.6 on 2019-11-04 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191101_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='userkey',
            name='host',
            field=models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Host'),
        ),
    ]