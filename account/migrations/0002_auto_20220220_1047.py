# Generated by Django 3.1.7 on 2022-02-20 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_customer',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_employee',
        ),
        migrations.AddField(
            model_name='user',
            name='is_add',
            field=models.BooleanField(default=False, verbose_name='Is add'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_cashier',
            field=models.BooleanField(default=False, verbose_name='Is cashier'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_daily_report',
            field=models.BooleanField(default=False, verbose_name='Is Daily report'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_expenses',
            field=models.BooleanField(default=False, verbose_name='Is expenses'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_expenses_report',
            field=models.BooleanField(default=False, verbose_name='Is Expenses report'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_monthly_report',
            field=models.BooleanField(default=False, verbose_name='Is Monthly report'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_registrar1',
            field=models.BooleanField(default=False, verbose_name='Is student registrar'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_registrar2',
            field=models.BooleanField(default=False, verbose_name='Is staff registrar'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_weekly_report',
            field=models.BooleanField(default=False, verbose_name='Is Weekly report'),
        ),
        migrations.AddField(
            model_name='user',
            name='nin',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_num',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
