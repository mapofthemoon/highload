from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

def first(request):
    return HttpResponse("hello blog")

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 1)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    total_posts = page_obj.paginator.count 

    return render(request, 'post_list.html', {
        'page_obj': page_obj,
        'total_posts': total_posts,
    })

def post_one(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()  

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  
            comment.author = request.user 
            comment.save()
            return redirect('post_one', id=post.id)  
    else:
        form = CommentForm()

    return render(request, 'post_one.html', {
        'post': post,
        'form': form,
        'comments': comments,
    })

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

class PostEditView(UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'post_edit.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return HttpResponseForbidden("You are not allowed to edit this post.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('post_one', kwargs={'id': self.object.id})

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return HttpResponseForbidden("You are not allowed to delete this post.")
        return super().dispatch(request, *args, **kwargs)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('post_list')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login') 
