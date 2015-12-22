from django.shortcuts import render

import models

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
    return render(request, 'post.html', {'post' : post})