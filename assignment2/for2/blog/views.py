from django.shortcuts import render
from .models import Post

def posts_by_tag(request, tag_name):
    specific_tag = tag_name
    posts_with_comments_and_tags = Post.objects.filter(tags__name=specific_tag).prefetch_related(
        'comments',
        'tags'
    ).select_related('author')

    if not posts_with_comments_and_tags:
        message = "No posts found for this tag."
    else:
        message = ""

    context = {
        'posts': posts_with_comments_and_tags,
        'tag_name': specific_tag,
        'message': message,
    }

    return render(request, 'blog/posts_by_tag.html', context)

def count_comments(post):
    cache_key = f'comments_count_{post.id}'
    count = cache.get(cache_key)
    if count is None:
        count = post.comment_set.count()
        cache.set(cache_key, count, timeout=60)  #ospanova aruzhan
    return count
