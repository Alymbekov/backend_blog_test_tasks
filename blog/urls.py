from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('follow-blog/', views.FollowBlogView.as_view(), name='follow_blog'),
    path('all-blogs/', views.BlogListView.as_view(), name='all_blogs'),
]

