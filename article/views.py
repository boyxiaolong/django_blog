from django.shortcuts import render

import models
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, HttpResponseForbidden
import logging
from django.core.context_processors import csrf
from django.views.generic import FormView,DetailView,ListView
import forms
from django.forms import ModelForm
from django.contrib import auth

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    post_list = models.Article.objects.all()
    return render(request, 'home.html', {'post_list' : post_list})
def about(request):
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
    print "blog_search"
    s = request.GET['search_text']
    if not s:
        return render(request, 'home.html')
    else:
        post_list = models.Article.objects.filter(title__contains=s)
        status = True
        if len(post_list) > 0:
            status = False
        return render(request, 'archives.html', {'post_list':post_list, 'error':status})

def create_blog(request):
    if not request.user.is_authenticated():
        return render(request, "registration/login.html")
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

def modify(request, id):
    if not request.user.is_authenticated():
        return render(request, "registration/login.html")
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