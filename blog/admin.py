from django.contrib import admin

from blog.models import PersonalBlog, Post, Follower

#TODO change to InlinesAdmin
admin.site.register(PersonalBlog)
admin.site.register(Post)
admin.site.register(Follower)
