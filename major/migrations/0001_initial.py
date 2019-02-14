# Generated by Django 2.1.4 on 2019-02-14 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MajorPlayback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('START', 'Playback started'), ('STOP', 'Playback ended')], max_length=10)),
                ('album', models.PositiveIntegerField(verbose_name='Album ID')),
                ('customer', models.PositiveIntegerField(verbose_name='User ID')),
            ],
        ),
    ]