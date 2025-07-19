from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from django.urls import reverse
from .models import Post, AboutUs
from django.core.paginator import Paginator
from .forms import ContactForm, RegisterForm , LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
import logging
# Create your views here.

def index(request):
    blog_title = "Latest Posts"

    # getting data from post model
    all_posts=Post.objects.all()

    # paginate
    paginator = Paginator(all_posts,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request,"blog/index.html",{'blog_title':blog_title,'page_obj':page_obj})

def detail(request,slug):

    try:
        # getting data from model by post id
        post = Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)
    except Post.DoesNotExist:
        raise Http404("Post Does not Exist")

    # logger = logging.getLogger("Testing")
    # logger.debug(f'post variable is {post}')
    return render(request,"blog/detail.html",{'post':post,'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse("blog:new_page_url"))

def new_url_view(request):
    return HttpResponse("This is the new URL")

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if form.is_valid():
            logger = logging.getLogger("TESTING")
            logger.debug(f'POST DATA is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']} ')
            success_message="Your Email has been sent!"
            return render(request,'blog/contact.html',{'form':form,'success_message':success_message})
        else:
            logger.debug('Form validation failure')
        return render(request,'blog/contact.html',{'form':form,'name':name,'email:':email,'message':message})
    return render(request,'blog/contact.html')

def about(request):
    about_content = AboutUs.objects.first()
    if about_content is None or not about_content.content:
        about_content = "Defautl content goes here" # Default text
    else:
        about_content = about_content.content
    return render(request,'blog/about.html',{'about_content':about_content})

def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
           user = form.save(commit=False) # user data created
           user.set_password(form.cleaned_data['password'])
           user.save()
           messages.success(request,"Registration Successfull. You can log in")
           return redirect('blog:login')
    return render(request,'blog/register.html',{'form':form})

def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                print("LOGIN SUCCESS")
                auth_login(request,user)
                return redirect("blog:dashboard") # redirect to dashboard
    return render(request,"blog/login.html",{'form':form})

def dashboard(request):
    blog_title = "MY Posts"
    return render(request,'blog/dashboard.html',{'blog_title':blog_title})

def logout(request):
    auth_logout(request)
    return redirect('blog:index')

def forgot_password(request):
    return render(request,'blog/forgot_password.html')