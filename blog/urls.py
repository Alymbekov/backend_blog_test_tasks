from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('follow-blog/', views.FollowBlogView.as_view(), name='follow_blog'),
    path('all-blog/', views.BlogListView.as_view(), name='all_blog'),
    path('add-follow/', views.FollowerView.as_view(), name='add_follow'),
    path('my-blog/', views.MyBlogView.as_view(), name='my_blog'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog'),
    path('post-create/', views.PostCreateView.as_view(), name='post_create'),
    path('post-read-view/', views.PostReadView.as_view(), name='post_read_view'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

]

