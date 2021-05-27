# from django.contrib import admin
# from . models import Scraper, ArticleSpider, ArticleThread, Article, CrawlerSet, CrawlerItem, ScraperAnalysis

# class ScraperAdmin(admin.ModelAdmin):
#     list_display = [
#         'user', 'data', 'workers', 'crawler_set',
#         'time_finished', 'terminated_process','is_finished', 'timestamp'
#     ]

# class ArticleSpiderAdmin(admin.ModelAdmin):
#     list_display = ['user', 'in_use']

# class ArticleThreadAdmin(admin.ModelAdmin):
#     list_display = ['user', 'in_use']

# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ['url', 'in_use']
#     search_fields = ['url']

# class CrawlerAdmin(admin.ModelAdmin):
#     list_display = ['user', 'is_finished', 'timestamp']

# class CrawlerItemAdmin(admin.ModelAdmin):
#     list_display = ('article_url', 'fqdn', 'download_latency', 'source_created_from','proxy', 'parser','article_status',
#                     'article_error_status', 'link_captured','redirect_urls', 'custom_url','redirect_reasons','handle_httpstatus_list', 'http_error', 'dns_error', 'timeout_error',
#                     'base_error', 'skip_url', 'in_use', 'timestamp',)
#     search_fields = ['article_url','fqdn', 'download_latency', 'handle_httpstatus_list', 'redirect_reasons','article_error_status', 'source_created_from', 'parser', 'custom_url']

#     # ordering = ('-date_parsed')

# admin.site.register(ScraperAnalysis)

# admin.site.register(Scraper, ScraperAdmin)
# admin.site.register(ArticleSpider, ArticleSpiderAdmin)
# admin.site.register(ArticleThread, ArticleThreadAdmin)
# admin.site.register(Article, ArticleAdmin)

# admin.site.register(CrawlerSet, CrawlerAdmin)
# admin.site.register(CrawlerItem, CrawlerItemAdmin)

