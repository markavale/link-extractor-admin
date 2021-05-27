
from . selector_helpers import (
    get_article_errors, get_article_fqdn_none, get_download_latency_not_none, get_article_timeout, get_base_error, get_no_content, get_dns_error, get_http_503, get_done_articles)
from ..models import (Scraper, ArticleSpider, ArticleThread,
                      Article, CrawlerSet, CrawlerItem, ScraperAnalysis)
from ..serializers import (ScraperSerializer, ArticleSpiderSerializer, ArticleThreadSerializer, ArticleSerializer,
                           CrawlerSetSerializer, CrawlerItemSerializer, ScraperAnalysisSerializer)
from ..pagination import (CrawlerItemPagination, ScraperPagination, ArticleSpiderPagination, ArticleThreadPagination, ArticlePagination,
                          ArticleErrorPagination)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page
# from django.views.decorators.vary import vary_on_cookie
import datetime
import time
import json
import math
import statistics
import re
import csv as c
from urllib.parse import urlparse
from django.conf import settings
from django.db.models import Avg
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# OVERVIEW / DASHBOARD


class ScraperAnalysisAPIView(APIView):

    def get(self, request):
        scrapers = get_scrapers(request)
        if scrapers.count() != 0:
            crawler_items = get_crawler_items(request)
            data = {}
            data['total_data'] = sum(
                list(map(lambda scraper: scraper.data, scrapers.all())))
            data['total_articles'] = sum(
                list(map(lambda scraper: scraper.get_total_articles(), scrapers.all())))
            data['total_avg_dl'] = round(statistics.mean(list(map(
                lambda scraper: scraper.crawler_set.get_avg_dl_latency(), scrapers.all()))), 2)
            data['total_successfull_parsed'] = sum(list(map(
                lambda scraper: scraper.crawler_set.get_total_parsed_article(), scrapers.all())))
            data['total_errors'] = sum(
                list(map(lambda scraper: scraper.crawler_set.get_total_error(), scrapers.all())))
            data['total_missed'] = sum(
                list(map(lambda scraper: scraper.get_total_missed_articles(), scrapers.all())))
            data['total_rounds_of_scraper'] = scrapers.count()

            # data['total_avg_dl_v1'] = scrapers.crawler_sets.all().aggregate(Avg(get_avg_dl_latency()))
            # data['total_avg_dl_v2'] = crawler_items.aggregate(Avg('download_latency'))

            return Response(data)
        else:
            return Response({"data": "No data available"})

# TOP WEBSITES FOR ERRORS, LATENCY


class ScraperErrorViewset(viewsets.ModelViewSet):
    serializer_class = CrawlerItemSerializer
    pagination_class = ArticleErrorPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_finished']
    search_fields = ['article_id', 'article_url', 'fqdn',
                     'article_error_status', 'proxy', 'user_agent']
    ordering = ['http_error', 'dns_error', 'timeout_error',
                'base_error', 'skip_url', 'source_created_from', 'timestamp']

    def get_queryset(self):
        # .values('scrapers')
        return CrawlerItem.objects.filter(article_status="Error")

    # @method_decorator(vary_on_cookie)
    # @method_decorator(cache_page(60*60))
    # def dispatch(self, *args, **kwargs):
    #     return super(ScraperErrorViewset, self).dispatch(*args, **kwargs)

    def get_permissions(self):
        # """
        # Instantiates and returns the list of permissions that this view requires.
        # """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]  # AllowAny
        elif self.action == 'create':
            permission_classes = [IsAdminUser]  # AllowAny
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class ScraperErrorAnalysisAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        data = {}
        errors = get_article_errors(request)

        print(errors)
        data['errors'] = errors.count()
        return Response(data)


# FUNCTION: returns the top 20 websites with its total errros
# @cache_page(CACHE_TTL)
@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def top_websites_error(request):
    data = {}
    websites = {}
    articles = get_article_errors(request)
    if articles is not None:
        collection = {}
        for item in articles:
            collection.setdefault(item.fqdn, []).append(item)
        results = []
        for k, v in sorted(collection.items(), key=lambda item: len(item[1]), reverse=True):
            results.append(
                {
                    "fqdn": k,
                    "total_errors": len(v),
                    "total_http_errors": len(list(filter(lambda item: item.http_error == 1, v))),
                    "total_dns_error": len(list(filter(lambda item: item.dns_error == 1, v))),
                    "total_timeout_error": len(list(filter(lambda item: item.timeout_error == 1, v))),
                    "total_base_error": len(list(filter(lambda item: item.base_error == 1, v))),
                    "total_missed_url": len(list(filter(lambda item: item.skip_url == 1, v)))
                }
            )
        return Response({"total":len(articles),"results": results})
    return Response({"data" "No article errors"})

@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def get_timeout_error_websites(request):
    data = {}
    websites = {}
    articles = get_article_timeout(request)
    # links = articles
    # with open('timeout.txt', 'w') as f:
    #     for article in articles:    
    #         f.write(article.article_url)
    #         f.write('\n')
    # links = list(map(lambda item:item.article_url, articles))
    # return Response({"Total Timeout": links})
    if articles is not None:
        collection = {}
        for item in articles:
            collection.setdefault(item.fqdn, []).append(item)
        results = []
        for k, v in sorted(collection.items(), key=lambda item: len(item[1]), reverse=True):
            # print(item.article_url)
            results.append(
                {
                    "fqdn": k,
                    "total_timeout_error": len(list(filter(lambda item: item.timeout_error == 1, v))),
                    
                    # "urls": list(map(lambda item:item.article_url, v))
                }
            )
        return Response({"total":len(articles),"results": results})
    return Response({"data" "No article errors"})

@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def base_error_websites(request):
    data = {}
    websites = {}
    articles = get_base_error(request)
    # links = articles
    # with open('timeout.txt', 'w') as f:
    #     for article in articles:    
    #         f.write(article.article_url)
    #         f.write('\n')
    # links = list(map(lambda item:item.article_url, articles))
    # return Response({"Total Timeout": links})
    header= ["FQDN", "Total Base Error"]
    if articles is not None:
        collection = {}
        for item in articles:
            collection.setdefault(item.fqdn, []).append(item)
        results = []
        for k, v in sorted(collection.items(), key=lambda item: len(item[1]), reverse=True):
            # print(item.article_url)
            results.append(
                {
                    "fqdn": k,
                    "total_base_error": len(list(filter(lambda item: item.base_error == 1, v))),
                    "Total System Link": len(list(filter(lambda item: item.source_created_from == "System Link", v))),
                    "Total Global Link": len(list(filter(lambda item: item.source_created_from == "Global Link", v)))
                }
            )
        with open('{}_Results.csv'.format("Base_Error"), 'w', encoding='UTF8') as f:
                writer = c.writer(f)

                # write the header
                writer.writerow(header)
                for data in results:
                    print(data)
                    writer.writerow([data['fqdn'], data['total_base_error']])
        return Response({"total": len(articles),"results": results})
    return Response({"data" "No article errors"})

@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def success_websites(request):
    data = {}
    websites = {}
    articles = get_done_articles(request)
    # links = articles
    # with open('timeout.txt', 'w') as f:
    #     for article in articles:    
    #         f.write(article.article_url)
    #         f.write('\n')
    # links = list(map(lambda item:item.article_url, articles))
    # return Response({"Total Timeout": links})
    header= ["FQDN", "Total Base Error"]
    if articles is not None:
        collection = {}
        for item in articles:
            collection.setdefault(item.fqdn, []).append(item)
        results = []
        for k, v in sorted(collection.items(), key=lambda item: len(item[1]), reverse=True):
            # print(item.article_url)
            results.append(
                {
                    "fqdn": k,
                    "total_base_error": len(list(filter(lambda item: item.article_status == "Done", v))),
                    "Total System Link": len(list(filter(lambda item: item.source_created_from == "System Link", v))),
                    "Total Global Link": len(list(filter(lambda item: item.source_created_from == "Global Link", v)))
                }
            )
        # with open('{}_Results.csv'.format("Base_Error"), 'w', encoding='UTF8') as f:
        #         writer = c.writer(f)

        #         # write the header
        #         writer.writerow(header)
        #         for data in results:
        #             print(data)
        #             writer.writerow([data['fqdn'], data['total_base_error']])
        return Response({"total": len(articles),"results": results})
    return Response({"data" "No article errors"})

@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def http_503_website(request):
    data = {}
    websites = {}
    articles = get_http_503(request)
    # links = articles
    # with open('timeout.txt', 'w') as f:
    #     for article in articles:    
    #         f.write(article.article_url)
    #         f.write('\n')
    # links = list(map(lambda item:item.article_url, articles))
    # return Response({"Total Timeout": links})
    if articles is not None:
        collection = {}
        for item in articles:
            collection.setdefault(item.fqdn, []).append(item)
        results = []
        for k, v in sorted(collection.items(), key=lambda item: len(item[1]), reverse=True):
            # print(item.article_url)
            results.append(
                {
                    "fqdn": k,
                    "total http error": len(list(filter(lambda item: item.http_error == 1, v))),
                }
            )
        return Response({"total": len(articles),"results": results})
    return Response({"data" "No article errors"})

@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def total_base_error(request):
    data = {}
    websites = {}
    articles = get_base_error(request)
    # links = articles
    # with open('timeout.txt', 'w') as f:
    #     for article in articles:    
    #         f.write(article.article_url)
    #         f.write('\n')
    # links = list(map(lambda item:item.article_url, articles))
    # return Response({"Total Timeout": links})
    if articles is not None:
        return Response({"total_base_errors": len(articles)})
    return Response({"data" "No article errors"})

@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def get_total_timeout(request):
    data = {}
    websites = {}
    articles = get_article_timeout(request)
    # links = articles
    # with open('timeout.txt', 'w') as f:
    #     for article in articles:    
    #         f.write(article.article_url)
    #         f.write('\n')
    # links = list(map(lambda item:item.article_url, articles))
    # return Response({"Total Timeout": links})
    if articles is not None:
        
        return Response({"total_timeout": len(articles)})
    return Response({"data" "No article errors"})

@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def no_content_websites(request):
    data = {}
    websites = {}
    articles = get_no_content(request)
    # links = articles
    # with open('timeout.txt', 'w') as f:
    #     for article in articles:    
    #         f.write(article.article_url)
    #         f.write('\n')
    # links = list(map(lambda item:item.article_url, articles))
    # return Response({"Total Timeout": links})
    header = ["WEBSITE", "TOTAL NO CONTENT", "WEBSITE TYPE"]
    if articles is not None:
        collection = {}
        for item in articles:
            collection.setdefault(item.fqdn, []).append(item)
        results = []
        for k, v in sorted(collection.items(), key=lambda item: len(item[1]), reverse=True):
            # print(item.article_url)
            results.append(
                {
                    "fqdn": k,
                    "total": len(list(filter(lambda item: item.base_error == 1, v))),
                }
            )
        
        # with open('{}_Results.csv'.format("NO_CONTENT"), 'w', encoding='UTF8') as f:
        #         writer = c.writer(f)

        #         # write the header
        #         writer.writerow(header)
        #         for data in results:
        #             print(data)
        #             writer.writerow([data['fqdn'], data['total']])
        return Response({"total":len(articles), "results": results})
    return Response({"data" "No article errors"})

@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def website_dns_error(request):
    data = {}
    websites = {}
    articles = get_dns_error(request)
    # links = articles
    # with open('timeout.txt', 'w') as f:
    #     for article in articles:    
    #         f.write(article.article_url)
    #         f.write('\n')
    # links = list(map(lambda item:item.article_url, articles))
    # return Response({"Total Timeout": links})
    # header = ["WEBSITE", "TOTAL NO CONTENT", "WEBSITE TYPE"]
    if articles is not None:
        collection = {}
        for item in articles:
            collection.setdefault(item.fqdn, []).append(item)
        results = []
        for k, v in sorted(collection.items(), key=lambda item: len(item[1]), reverse=True):
            # print(item.article_url)
            results.append(
                {
                    "fqdn": k,
                    "total": len(list(filter(lambda item: item.dns_error == 1, v))),
                }
            )
        
        # with open('{}_Results.csv'.format("NO_CONTENT"), 'w', encoding='UTF8') as f:
        #         writer = c.writer(f)

        #         # write the header
        #         writer.writerow(header)
        #         for data in results:
        #             print(data)
        #             writer.writerow([data['fqdn'], data['total']])
        return Response({"total":len(articles), "results": results})
    return Response({"data" "No article errors"})

# FUNCTION: returns the top 20 websites with its total errros
# @cache_page(CACHE_TTL)


@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def website_download_latency(request):
    data = {}
    websites = {}
    articles = get_download_latency_not_none(request)
    # statistics.mean()
    if articles is not None:
        collection = {}
        for item in articles:
            collection.setdefault(item.fqdn, []).append(item)
        results = []
        for k, v in sorted(collection.items(), key=lambda item: round(statistics.mean(list(map(lambda data: data.download_latency, item[1]))), 2), reverse=True):
            results.append(
                {
                    "fqdn": k,
                    "total_objects": len(v),
                    "download_latency_objects": [round(x.download_latency, 2) for x in v],
                    "average_download_latency": round(statistics.mean(list(map(lambda data: data.download_latency, v))), 2)
                }
            )
        return Response({"results": results})
    return Response({"data" "No article errors"})

### TEST ###


@permission_classes([IsAdminUser, ])
@api_view(['GET', ])
def test_view(request):
    # articles = Scraper.objects.filter()
    return Response({"data": "data"})
### ========================= CBV MODELVIEWSET ========================= ###


'''
    CBV's FOR SCRAPER ANALYSIS
'''


class ScraperAnalysisViewset(viewsets.ModelViewSet):
    serializer_class = ScraperAnalysisSerializer

    def get_queryset(self):
        return ScraperAnalysis.objects.all()  # .values('scrapers')

    # @method_decorator(vary_on_cookie)
    # @method_decorator(cache_page(60*60))
    def dispatch(self, *args, **kwargs):
        return super(ScraperAnalysisViewset, self).dispatch(*args, **kwargs)

    def get_permissions(self):
        # """
        # Instantiates and returns the list of permissions that this view requires.
        # """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]  # AllowAny
        elif self.action == 'create':
            permission_classes = [IsAdminUser]  # AllowAny
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


'''
    CBVs FOR SCRAPER, ARTICLE SPIDER, ARTICLE THREAD, ARTICLE
    MAIN OBJECT => SCRAPER
        * CHILDERN OBJECTS *
            ARTICLE SPIDER => MANY TO MANY
                ARTICLE THREAD => MANY TO MANY
                    ARTICLE
'''
# CBV SCRAPER


class ScraperViewset(viewsets.ModelViewSet):
    pagination_class = ScraperPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filter_backends = [DjangoFilterBackend,
    #                    filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_finished']
    search_fields = ['user', 'workers']
    ordering = ['user', 'time_finished']
    serializer_class = ScraperSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Scraper.objects.prefetch_related('data', 'workers',
                                                'info_log',
                                                'error_log',
                                                'time_finished',
                                                'terminated_process',
                                                'timestamp').all()  # .all()  # .order_by('-timestamp')

    # @method_decorator(vary_on_cookie)
    # @method_decorator(cache_page(60*60))
    def dispatch(self, *args, **kwargs):
        return super(ScraperViewset, self).dispatch(*args, **kwargs)

    def get_permissions(self):
        # """
        # Instantiates and returns the list of permissions that this view requires.
        # """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]  # AllowAny
        elif self.action == 'create':
            permission_classes = [IsAdminUser]  # AllowAny
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

# CBV ARTICLE SPIDER


class ArticleSpiderViewset(viewsets.ModelViewSet):
    serializer_class = ArticleSpiderSerializer
    pagination_class = ArticleSpiderPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['in_use']
    lookup_field = 'id'

    def get_queryset(self):
        return ArticleSpider.objects.all()

    def get_permissions(self):
        # """
        # Instantiates and returns the list of permissions that this view requires.
        # """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]  # AllowAny
        elif self.action == 'create':
            permission_classes = [IsAdminUser]  # AllowAny
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

# CBV ARTICLE THREAD


class ArticleThreadViewset(viewsets.ModelViewSet):
    serializer_class = ArticleThreadSerializer
    pagination_class = ArticleThreadPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['in_use']
    lookup_field = 'id'

    def get_queryset(self):
        return ArticleThread.objects.all()

    def get_permissions(self):
        # """
        # Instantiates and returns the list of permissions that this view requires.
        # """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]  # AllowAny
        elif self.action == 'create':
            permission_classes = [IsAdminUser]  # AllowAny
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

# CBV ARTICLE


class ArticleViewset(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_backends = [filters.SearchFilter]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['in_use']
    search_fields = ['article_id', 'url']
    lookup_field = 'id'

    def get_queryset(self):
        return Article.objects.all()

    def get_permissions(self):
        # """
        # Instantiates and returns the list of permissions that this view requires.
        # """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]  # AllowAny
        elif self.action == 'create':
            permission_classes = [IsAdminUser]  # AllowAny
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


'''
    @ SCRAPER ANALYSIS FUNCTION HELPERS
'''
# GET or CREATE: scraper analysis function for creating or getting the first object


def get_scraper_analysis(request):
    scraper_analysis = ScraperAnalysis.objects.all()
    if scraper_analysis.exists():
        return scraper_analysis[0]
    else:
        obj = ScraperAnalysis.objects.create()
        return obj


'''
    ALL function helpers for SCRAPER OBJECT
    SCRAPER             => get or create SCRAPER object
    ARTICLE SPIDER      => get or create ARTICLE SPIDER object
    ARTICLE THREAD      => get or create ARTICLE THREAD object
    ARTICLE             => save article
'''
# FUNCTION for returning SCRAPER not finish. If exists retrieve, else generate new SCRAPER object is_finished = False.


def scraper_obj_not_finish(request):
    try:
        crawler_set = get_crawler_crawler_set(request)
        scraper_obj = Scraper.objects.filter(
            user=request.user, is_finished=False)
        if scraper_obj.exists():
            scraper = scraper_obj[0]
        else:
            scraper = Scraper.objects.create(
                user=request.user, is_finished=False)
    except Exception as e:
        print(e)

    return scraper

# FUNCTION for returning article spider not in use. If exists retrive, else generate new ARTICLE SPIDER object in_use = False.


def get_article_spider_not_in_use(request):
    spider_obj = ArticleSpider.objects.filter(user=request.user, in_use=False)
    if spider_obj.exists():
        spider = spider_obj[0]
    else:
        spider = ArticleSpider.objects.create(user=request.user, in_use=False)
    return spider

# FUNCTION for returning for not in use article threads. If exists retrieve, else generate new THREAD object in_use = False.


def get_article_thread_not_in_use(request):
    thread_obj = ArticleThread.objects.filter(user=request.user, in_use=False)
    if thread_obj.exists():
        thread = thread_obj[0]
    else:
        thread = ArticleThread.objects.create(user=request.user, in_use=False)
    return thread

# FUNCTION for returning not in use artilces


def get_articles_not_in_use(request):
    articles = Article.objects.filter(in_use=False)
    if articles.exists():
        return articles
    else:
        return Response({"Error": "No articles available"})

# FUNCTION for saving articles


def add_article(request, articles):
    for article in articles:
        serializer = ArticleSerializer(data=article)
        if serializer.is_valid():
            serializer.save()
            print("article saved!!")
    article_objs = Article.objects.filter(in_use=False)
    return


'''
    ALL function helpers for CRAWLER SET OBJECT
    CRAWLER SET         => get or create CRAWLER SET object

'''
# FUNCTION for returning crawler set not finish. If exists retrieve, else generate new CRAWLER SET is_finished = False.


def get_crawler_crawler_set(request):
    crawler_set = CrawlerSet.objects.filter(
        user=request.user, is_finished=False)
    if crawler_set.exists():
        crawler_obj = crawler_set[0]
    else:
        crawler_obj = CrawlerSet.objects.create(
            user=request.user, is_finished=False)
    return crawler_obj


def get_crawler_items(request):
    try:
        articles = CrawlerItem.objects.filter(downdload_latency != None)
        return articles
    except Exception as e:
        return Response({"error": e})


'''
    Scraper analysis section

'''


def get_scrapers(request):
    try:
        scrapers = Scraper.objects.filter(is_finished=True)
        return scrapers
    except Exception as e:
        return Response({"error": e})


def get_crawler_sets(request):
    try:
        article_data = CrawlerSet.objects.filter(is_finished=True)
        return article_data
    except:
        return Response({"data": "No data available"})


def get_articles(request):
    try:
        articles = Article.objects.filter(in_use=True)
        return articles
    except:
        return Response({"data": "No articles available"})
