# Generated by Django 5.0.4 on 2024-05-08 23:00

import django.db.models.deletion
import usage.models.models_validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usage', '0003_submodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidationReference',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='氏名')),
            ],
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.CharField(max_length=20, verbose_name='文字列長制限')),
                ('positive_even', models.IntegerField(validators=[usage.models.models_validation.validate_even, usage.models.models_validation.validate_positive], verbose_name='正の偶数')),
                ('unique', models.CharField(max_length=20, unique=True, verbose_name='ユニーク制限')),
                ('choices', models.CharField(choices=[(1, 'a'), (2, 'b'), (3, 'c')], max_length=20, verbose_name='選択式')),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usage.validationreference', verbose_name='参照先')),
            ],
        ),
    ]
