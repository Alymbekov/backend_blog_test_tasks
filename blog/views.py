from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from blog.models import Post, PersonalBlog


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


# class FollowerView(LoginRequiredMixin, CreateView):
#     form_class = FollowerForm
#     success_url = reverse_lazy('blog:follow_blog')
#
#     def form_valid(self, form):
#         super(FollowerView, self).form_valid()



