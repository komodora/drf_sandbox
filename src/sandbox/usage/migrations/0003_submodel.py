# Generated by Django 5.0.4 on 2024-05-03 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0002_role_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=50, verbose_name='タイトル')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
