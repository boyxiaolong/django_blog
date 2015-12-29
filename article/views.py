from django.shortcuts import render

import models
from django.contrib.syndication.views import Feed
from django.http import HttpResponse, HttpResponseForbidden
import logging
from django.core.context_processors import csrf
from django.views.generic import FormView,DetailView,ListView
import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.forms import ModelForm

logger = logging.getLogger(__name__)

class ArticleForm(ModelForm):
    class Meta:
        model = models.Article
        fields = '__all__'
        widgets = {
            'title' : SummernoteInplaceWidget(),
            'content' : SummernoteWidget(),
            'category' : SummernoteInplaceWidget(),
        }
# Create your views here.
def home(request):
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
    return render(request, 'post_modify.html', {'post' : post, 'images':images})
def archives(request):
	try:
		post_list = models.Article.objects.all()
	except models.Article.DoesNotExist:
		return Http404
	return render(request, 'archives.html', {'post_list':post_list,
		'error':False})
def search_tag(request, tag) :
    try:
        post_list = models.Article.objects.filter(category__iexact = tag) #contains
    except models.Article.DoesNotExist :
        raise Http404
    return render(request, 'tag.html', {'post_list' : post_list})

def blog_search(request):
	if 's' in request.GET:
		s = request.GET['s']
		if not s:
			return render(request, 'home.html')
		else:
			post_list = models.Article.objects.filter(title__contains=s)
			status = True
			if len(post_list) > 0:
				status = False
			return render(request, 'archives.html', {'post_list':post_list, 'error':status})
		return redirect('/')

def newblog(request):
    if request.POST:
        c = {}
        c.update(csrf(request))
        title = request.POST.get('title', "")
        content = request.POST.get('content', "")
        tag = request.POST.get("tag", "")
        print title, " ", content, " ", tag
        if len(title) > 0:
            new_post,create = models.Article.objects.update_or_create(title=title, category=tag, content=content)
            new_post.save()
            return render(request, 'post.html', {'post' : new_post})
        return render(request, "post_success.html", c)
    else:
        form = ArticleForm()
        return render(request, 'newblog.html', {'form':form})
def modify(request, id):
    print "try to modify ", request
    try:
        post = models.Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    if request.POST:
        title = request.POST.get('title', "")
        content = request.POST.get('content', "")
        tag = request.POST.get("tag", "")
        post.title = title
        post.content = content
        post.tag = tag
        post.save()
        return render(request, "post_modify.html", {'post':post})
    else:
        form = ArticleForm()
        return render(request, "edit.html", {'post':post, 'form':form})
class RSSFeed(Feed) :
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return models.Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content
def upload_pic(request):
    if request.method == 'POST':
        form = forms.ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = models.ExampleModel()
            m.model_pic = form.cleaned_data['image']
            m.save()
            return HttpResponse('image upload success')
    return HttpResponseForbidden('allowed only via POST')
