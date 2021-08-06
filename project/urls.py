"""wavepool URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from news import views as news_views
from wavepool import views as wavepool_views
from api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', news_views.front_page, name='home'),
    path('news/<int:newspost_id>/', news_views.newspost_detail, name='newspost_detail'),
    path('news/archive/', news_views.archive, name='newspost_archive'),
    path('instructions/', wavepool_views.instructions, name='instructions'),
    path('api/v1/news/', api_views.NewsPostApi.as_view(), name='api_news')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
