from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index'),
    path('follow-blog/', views.FollowBlogView.as_view(), name='follow_blog'),
    path('all-blog/', views.BlogListView.as_view(), name='all_blog'),
    path('add-follow/', views.FollowerView.as_view(), name='add_follow'),
    path('my-blog/', views.MyBlogView.as_view(), name='my_blog'),

]

