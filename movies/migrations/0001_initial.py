# Generated by Django 4.2.8 on 2024-05-22 00:21

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
            name='Genre',
            fields=[
                ('genre_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('overview', models.TextField(null=True)),
                ('popularity', models.FloatField(null=True)),
                ('backdrop_path', models.TextField(null=True)),
                ('poster_path', models.TextField(null=True)),
                ('release_date', models.DateField(null=True)),
                ('vote_average', models.FloatField(null=True)),
                ('adult', models.BooleanField(default=False)),
                ('embedding', models.JSONField(blank=True, null=True)),
                ('genre_embedding', models.JSONField(blank=True, null=True)),
                ('genres', models.ManyToManyField(related_name='movies', to='movies.genre')),
                ('like_users', models.ManyToManyField(related_name='like_movies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=250)),
                ('score', models.FloatField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
