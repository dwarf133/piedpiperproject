# Generated by Django 4.0.5 on 2022-06-26 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_tableanalyzecompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='other_name',
            field=models.TextField(blank=True, null=True, verbose_name='Другие варианты названий компании'),
        ),
    ]