from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('username', 'email')
        permissions = (('can_view_profile', 'Can view profile'),)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups', 
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions', 
        blank=True,
    )

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),  #Aruzhan Ospanova 
        ]

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='posts')

    class Meta:
        indexes = [
            models.Index(fields=['author', 'created_at']),  # Composite index on author and created_at
        ]

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['post', 'created_at']),  # Composite index for post and created_at
        ]
