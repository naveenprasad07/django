from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.urls import reverse
from .models import Post

# Create your views here.

def index(request):
    blog_title = "Latest Posts"
    posts=Post.objects.all()
    return render(request,"blog/index.html",{'blog_title':blog_title,'posts':posts})

def detail(request,slug):

    try:
        # getting data from model by post id
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("Post Does not Exist")

    # logger = logging.getLogger("Testing")
    # logger.debug(f'post variable is {post}')
    return render(request,"blog/detail.html",{'post':post})

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))

def new_url_view(request):
    return HttpResponse("This is the new URL")
