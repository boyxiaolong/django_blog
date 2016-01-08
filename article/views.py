from django.shortcuts import render

import models
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
import logging
from django.core.context_processors import csrf
from django.views.generic import FormView,DetailView,ListView
import forms
from django.forms import ModelForm
from django.contrib import auth
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import get_current_site

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    post_list = models.Article.objects.all()
    return render(request, 'home.html', {'post_list' : post_list})

def about(request):
    print "about"
    return render(request, 'about.html')

def detail(request, id):
    try:
        post = models.Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post_modify.html', {'post' : post})

def archives(request):
	try:
		post_list = models.Article.objects.all()
	except models.Article.DoesNotExist:
		return Http404
	return render(request, 'archives.html', {'post_list':post_list,
		'error':False})

def search_category(request, category) :
    try:
        post_list = models.Article.objects.filter(category__iexact = category) #contains
    except models.Article.DoesNotExist :
        raise Http404
    return render(request, 'tag.html', {'post_list' : post_list})

def blog_search(request):
    s = request.GET['search_text']
    if not s:
        return render(request, 'home.html')
    else:
        post_list = models.Article.objects.filter(title__contains=s)
        status = True
        if len(post_list) > 0:
            status = False
        return render(request, 'archives.html', {'post_list':post_list, 'error':status})

@login_required
def create_blog(request):
    if request.POST:
        c = {}
        c.update(csrf(request))
        title = request.POST.get('title', "")
        tag = request.POST.get("tag", "")
        form = forms.ArticleForm(request.POST)
        content = ""
        if form.is_valid():
            content = form.cleaned_data['content']
        if len(title) > 0:
            new_post,create = models.Article.objects.update_or_create(title=title, category=tag, content=content)
            new_post.save()
            return render(request, 'post_modify.html', {'post' : new_post})
        return render(request, "post_success.html", c)
    else:
        form = forms.ArticleForm()
        return render(request, 'newblog.html', {'form':form})

@login_required
def modify(request, id):
    try:
        post = models.Article.objects.get(id=str(id))
    except models.Article.DoesNotExist:
        raise Http404
    if request.POST:
        title = request.POST.get('title', "")
        content = request.POST.get('content', "")
        category = request.POST.get("category", "")
        post.title = title
        post.content = content
        post.category = category
        post.save()
        return render(request, "post_modify.html", {'post':post})
    else:
        form = forms.ArticleWigetForm(instance=post)
        return render(request, "edit.html", {'post':post, 'form':form})

class PostRssFeed(Feed):
    feed_type = Atom1Feed
    title = u'AllenZhao \'s Blog'
    link = 'http://' + get_current_site(None).domain
    description = u'Welcome to AllenZhao \'s Blog'
    author = 'AllenZhao'

    def items(self):
        return models.Article.objects.all().order_by('-date_time')[:10]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content

class PostAtomFeed(PostRssFeed):
    feed_type = Atom1Feed
    subtitle = PostRssFeed.item_description