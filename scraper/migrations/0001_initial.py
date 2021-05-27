# Generated by Django 3.1.1 on 2021-05-27 06:53

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
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('in_use', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleSpider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_use', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CrawlerItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_url', models.URLField()),
                ('custom_url', models.URLField(blank=True, null=True)),
                ('fqdn', models.CharField(blank=True, max_length=255, null=True)),
                ('total_links', models.IntegerField()),
                ('download_latency', models.FloatField(blank=True, null=True)),
                ('article_status', models.CharField(choices=[('Done', 'Done'), ('Error', 'Error'), ('Processing', 'Processing'), ('Queued', 'Queued')], max_length=100)),
                ('article_error_status', models.CharField(blank=True, max_length=100, null=True)),
                ('link_captured', models.CharField(blank=True, max_length=255, null=True)),
                ('http_error', models.IntegerField(default=0)),
                ('dns_error', models.IntegerField(default=0)),
                ('timeout_error', models.IntegerField(default=0)),
                ('base_error', models.IntegerField(default=0)),
                ('skip_url', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('in_use', models.BooleanField(default=False)),
                ('proxy', models.CharField(blank=True, max_length=255, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=400, null=True)),
                ('source_created_from', models.CharField(blank=True, max_length=255, null=True)),
                ('parser', models.CharField(blank=True, max_length=255, null=True)),
                ('handle_httpstatus_list', models.CharField(blank=True, max_length=500, null=True)),
                ('redirect_urls', models.CharField(blank=True, max_length=500, null=True)),
                ('redirect_reasons', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CrawlerSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_finished', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('crawlers', models.ManyToManyField(to='scraper.CrawlerItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Scraper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.IntegerField(default=0)),
                ('workers', models.IntegerField(default=0)),
                ('info_log', models.TextField(blank=True, null=True)),
                ('error_log', models.TextField(blank=True, null=True)),
                ('time_finished', models.TimeField(blank=True, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('terminated_process', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('crawler_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='scraper.crawlerset')),
                ('spiders', models.ManyToManyField(to='scraper.ArticleSpider')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ScraperAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scrapers', models.ManyToManyField(to='scraper.Scraper')),
            ],
            options={
                'verbose_name_plural': 'Scraper Analysis',
            },
        ),
        migrations.AddField(
            model_name='crawleritem',
            name='links',
            field=models.ManyToManyField(to='scraper.Links'),
        ),
        migrations.CreateModel(
            name='ArticleThread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_use', models.BooleanField(default=False)),
                ('articles', models.ManyToManyField(to='scraper.Article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='articlespider',
            name='thread_crawlers',
            field=models.ManyToManyField(to='scraper.ArticleThread'),
        ),
        migrations.AddField(
            model_name='articlespider',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
