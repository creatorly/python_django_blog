# Generated by Django 2.1.4 on 2018-12-19 07:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.EmailField(max_length=20)),
                ('email', models.EmailField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('add_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
            ],
        ),
    ]
