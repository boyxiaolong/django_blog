"""django_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'article.views.home'),
    url(r'^home/$', 'article.views.home', name='home'),
    url(r'^about/$', 'article.views.about', name='about'),
    url(r'^(?P<id>\d+)/$', 'article.views.detail', name='detail'),
    url(r'^archives/$', 'article.views.archives', name = 'archives'),
    url(r'^(?P<category>[\w\-]+)/$', 'article.views.search_category', name = 'search_category'),
    url(r'^search/','article.views.blog_search', name = 'search'),
    url(r'^/newblog/$', 'article.views.newblog', name='newblog'),
    url(r'^modify/(?P<id>\d+)/$', 'article.views.modify', name="modify"),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
