from django.contrib import admin
from .models import Profile, Post, FollowersCount, LikePost

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FollowersCount)
admin.site.register(LikePost)