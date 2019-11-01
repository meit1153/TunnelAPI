# Generated by Django 2.2.6 on 2019-11-01 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userkey',
            options={'verbose_name': 'UserKey', 'verbose_name_plural': 'UserKey'},
        ),
        migrations.RemoveField(
            model_name='assignport',
            name='key',
        ),
        migrations.AlterField(
            model_name='assignport',
            name='assigned_port',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='assignport',
            name='user_ip',
            field=models.CharField(db_index=True, max_length=50, verbose_name='User_IP'),
        ),
        migrations.DeleteModel(
            name='AvailablePort',
        ),
    ]
