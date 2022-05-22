# Generated by Django 4.0.3 on 2022-04-04 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('squat_weight', models.IntegerField(default=0)),
                ('squat_reps', models.IntegerField(default=0)),
                ('deadlift_weight', models.IntegerField(default=0)),
                ('deadlift_reps', models.IntegerField(default=0)),
                ('bench_weight', models.IntegerField(default=0)),
                ('bench_reps', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField()),
                ('message', models.CharField(max_length=500)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipient', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyDiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField()),
                ('protein', models.IntegerField(default=0)),
                ('carbs', models.IntegerField(default=0)),
                ('fats', models.IntegerField(default=0)),
                ('attended_gym', models.BooleanField(default=False)),
                ('weight', models.IntegerField(default=0)),
                ('exercises', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='HealthWebsite.exerciselist')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]