from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from blog.forms import PostCreateForm
from blog.models import Post, PersonalBlog, Follower, PostsRead

User = get_user_model()


class IndexPageView(LoginRequiredMixin, TemplateView):
    """Show all posts from blog sorting with created_at data
    """
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexPageView, self).get_context_data()
        context['news'] = Post.objects.filter(blog__follower__user=self.request.user, posts_read__isnull=True).order_by('-created_at')
        return context


class FollowBlogView(LoginRequiredMixin, ListView):
    """Show all the blog I subscribe to
    """
    model = PersonalBlog
    template_name = 'blog/follow_blog.html'

    def get_queryset(self):
        queryset = super(FollowBlogView, self).get_queryset()
        queryset = queryset.filter(follower__user=self.request.user)
        return queryset


class BlogListView(LoginRequiredMixin, ListView):
    """Get all blog without my(author)
    """
    model = PersonalBlog
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        queryset = PersonalBlog.objects.filter().exclude(author=self.request.user)
        return queryset


class MyBlogView(LoginRequiredMixin, ListView):
    """Show only authors blog
    """
    model = PersonalBlog
    template_name = 'blog/my_blog.html'

    def get_queryset(self):
        queryset = PersonalBlog.objects.filter(author=self.request.user)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Detail blog object,
    in detail also show posts
    """
    model = PersonalBlog
    template_name = 'blog/blog_details.html'


class FollowerView(LoginRequiredMixin,  View):
    """Follow and Unfollow functional,
    after add or remove follow view redirect to
    success_url
    """
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
            # deleted posts reads object if blog.id == post_blog_id
            PostsRead.objects.filter(user=self.request.user, post__blog_id=blog.id).delete()
            return redirect(self.success_url)

        return redirect(self.success_url)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create Post, automatically choice author and blog
    """
    template_name = 'blog/post_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:my_blog')

    def form_valid(self, form):
        form.instance.blog = PersonalBlog.objects.filter(author=self.request.user).first()
        return super(PostCreateView, self).form_valid(form)


class PostReadView(LoginRequiredMixin, View):
    template_name = 'blog/postread.html'
    success_url = reverse_lazy('blog:index')

    def get(self, request):
        posts = PostsRead.objects.filter(user=self.request.user)
        return render(request, self.template_name, locals())

    def post(self, request, *args, **kwargs):
        if request.POST.get('status'):
            post = Post.objects.filter(pk=request.POST.get('post')).first()
            post_read = PostsRead(user=self.request.user, post=post, is_read=True)
            post_read.save()
            return redirect(self.success_url)

        elif not request.POST.get('status'):
            post = Post.objects.get(pk=request.POST.get('post'))
            post_read = PostsRead.objects.filter(user=self.request.user, post=post)
            post_read.delete()
            return redirect(self.success_url)

        else:
            raise ValueError("Error")


class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'blog/post_detail.html'
    model = Post



