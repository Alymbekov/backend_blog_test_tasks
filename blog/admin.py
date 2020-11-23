from django.contrib import admin

from blog.models import PersonalBlog, Post, Follower, PostsRead

#TODO change to InlinesAdmin
admin.site.register(PersonalBlog)
admin.site.register(Post)
admin.site.register(Follower)
admin.site.register(PostsRead)

