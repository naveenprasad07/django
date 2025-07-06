from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse
# Create your views here.
def index(request):
    return render(request,"blog/index.html")

def detail(request,post_id):
    return render(request,"blog/detail.html")

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))

def new_url_view(request):
    return HttpResponse("This is the new URL")
