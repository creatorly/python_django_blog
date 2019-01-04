# Generated by Django 2.1.4 on 2018-12-20 06:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_users_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('add_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('add_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='分类创建日期')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('add_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Articles')),
            ],
        ),
        migrations.AddField(
            model_name='users',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='comments',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Users'),
        ),
        migrations.AddField(
            model_name='category',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Users'),
        ),
        migrations.AddField(
            model_name='articles',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Users'),
        ),
        migrations.AddField(
            model_name='articles',
            name='category',
            field=models.ManyToManyField(to='cms.Category'),
        ),
    ]
