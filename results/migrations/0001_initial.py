# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-24 19:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import results.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(choices=[('DK', 'DraftKings'), ('FD', 'FanDuel')], max_length=2)),
                ('sport', models.CharField(choices=[('NFL', 'National Football League'), ('CFB', 'College Football'), ('NBA', 'National Basketball Association'), ('CBB', 'College Basketball'), ('NHL', 'National Hockey League'), ('MMA', 'Mixed Martial Arts'), ('MLB', 'Major League Baseball'), ('SOC', 'Soccer'), ('PGA', 'Golf'), ('LOL', 'eSports'), ('NAS', 'Nascar')], max_length=3)),
                ('contest_type', models.CharField(choices=[('50/50', 'Double-Up (50/50)'), ('H2H', 'Head-to-Head'), ('3X', 'Triple-Up'), ('5X', 'Quintuple-Up'), ('10X', '10x Multiplier'), ('WTA', 'Winner Take All'), ('LG', 'League'), ('SAT', 'Satellite/Qualifer'), ('QUA', 'Qualifer'), ('GPP', 'Guaranteed Prize Pool'), ('FRE', 'Freeroll'), ('PRI', 'Private'), ('NA', 'Unknown')], max_length=3)),
                ('date', models.DateField(verbose_name='contest date')),
                ('time', models.TimeField(default='00:00', verbose_name='contest time')),
                ('single_entry', models.BooleanField(default=False)),
                ('original_contest_name', models.CharField(max_length=128)),
                ('contest_name', models.CharField(max_length=128)),
                ('points', models.DecimalField(decimal_places=2, max_digits=5)),
                ('entry_fee', models.DecimalField(decimal_places=2, max_digits=7)),
                ('winnings', models.DecimalField(decimal_places=2, max_digits=10)),
                ('place', models.IntegerField(default=0)),
                ('contest_entries', models.IntegerField(default=1)),
                ('entry_num', models.IntegerField(default=1)),
                ('your_num_entries', models.IntegerField(default=0)),
                ('opponent', models.CharField(max_length=30, null=True)),
                ('prize_pool', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ResultsFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=results.utils.get_upload_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DkResults',
            fields=[
                ('results_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='results.Results')),
                ('winnings_tix', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
            ],
            bases=('results.results',),
        ),
        migrations.CreateModel(
            name='FdResults',
            fields=[
                ('results_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='results.Results')),
                ('entry_id', models.CharField(max_length=11)),
                ('link', models.URLField()),
            ],
            bases=('results.results',),
        ),
        migrations.AddField(
            model_name='results',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
