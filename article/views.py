from django.shortcuts import render

import models
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, HttpResponseForbidden
import logging
from django.core.context_processors import csrf
from django.views.generic import FormView,DetailView,ListView
import forms
from django.forms import ModelForm

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    print("home")
    post_list = models.Article.objects.all()
    return render(request, 'home.html', {'post_list' : post_list})
def about(request):
	return render(request, 'about.html')
def detail(request, id):
    print "try detail"
    try:
        post = models.Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    images = models.ExampleModel.objects.filter(article=post)
    return render(request, 'post.html', {'post' : post})
def archives(request):
	try:
		post_list = models.Article.objects.all()
	except models.Article.DoesNotExist:
		return Http404
	return render(request, 'archives.html', {'post_list':post_list,
		'error':False})
def search_tag(request, tag) :
    try:
        print "111"
        post_list = models.Article.objects.filter(category__iexact = tag) #contains
    except models.Article.DoesNotExist :
        raise Http404
    return render(request, 'tag.html', {'post_list' : post_list})

def blog_search(request):
    s = request.GET['s']
    if not s:
        print request
        return render(request, 'home.html')
    else:
        post_list = models.Article.objects.filter(title__contains=s)
        status = True
        if len(post_list) > 0:
            status = False
        return render(request, 'archives.html', {'post_list':post_list, 'error':status})

def newblog(request):
    print "newlog"
    if request.POST:
        print "there"
        c = {}
        c.update(csrf(request))
        title = request.POST.get('title', "")
        content = request.POST.get('content', "")
        tag = request.POST.get("tag", "")
        form = forms.ArticleForm(request.POST)
        print title, " ", content, " ", tag
        if len(title) > 0:
            new_post,create = models.Article.objects.update_or_create(title=title, category=tag, content=content)
            new_post.save()
            return render(request, 'post.html', {'post' : new_post})
        return render(request, "post_success.html", c)
    else:
        print "here"
        form = forms.ArticleForm()
        return render(request, 'newblog.html', {'form':form})
def modify(request, id):
    print "try to modify ", request
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
        form = forms.AnotherForm()
        return render(request, "edit.html", {'post':post, 'form':form})
