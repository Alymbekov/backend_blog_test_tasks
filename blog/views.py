from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView

from blog.models import Post, PersonalBlog, Follower

User = get_user_model()


class IndexPageView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data()
        context['news'] = Post.objects.filter(blog__follower__user=self.request.user)
        return context


class FollowBlogView(LoginRequiredMixin, ListView):
    model = PersonalBlog
    template_name = 'blog/follow_blog.html'

    def get_queryset(self):
        queryset = super(FollowBlogView, self).get_queryset()
        queryset = queryset.filter(follower__user=self.request.user)
        return queryset


class BlogListView(LoginRequiredMixin, ListView):
    model = PersonalBlog
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        queryset = PersonalBlog.objects.filter().exclude(author=self.request.user)
        return queryset


class MyBlogView(LoginRequiredMixin, ListView):
    model = PersonalBlog
    template_name = 'blog/my_blog.html'

    def get_queryset(self):
        queryset = PersonalBlog.objects.filter(author=self.request.user)
        return queryset


class FollowerView(LoginRequiredMixin,  View):
    success_url = reverse_lazy('blog:follow_blog')

    def get(self, request):
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        is_follow = request.POST.get('follow')
        is_un_follow = request.POST.get('unfollow')
        blog = PersonalBlog.objects.filter(id=request.POST.get('blog')).first()
        if is_follow:
            follower, status = Follower.objects.get_or_create(user=self.request.user)
            follower.save()
            follower.blog.add(blog)
            return redirect(self.success_url)
        elif is_un_follow:
            follower = Follower.objects.filter(user=self.request.user).first()
            follower.blog.remove(blog)
            return redirect(self.success_url)

        return redirect(self.success_url)





