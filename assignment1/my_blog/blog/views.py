from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from blog.models import Post

def first(request):
   return HttpResponse("hello bl0g")


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})


def post_one(request, id):
    post = get_object_or_404(Post, id=id)  
    return render(request, 'post_one.html', {'post': post})
