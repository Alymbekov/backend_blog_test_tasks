from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from django.urls import reverse

from blog.tasks import send_notification_to_followers_task

User = get_user_model()


class PersonalBlog(models.Model):
    """A user can only have one blog"""
    title = models.CharField(max_length=255)
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personalblog')

    def __str__(self):
        return f'{self.author.username}{self.title}'

    def is_follow(self, author):
        if self.follower_set.all().filter(user=author).exists():
            return True
        else:
            return False


class Post(models.Model):
    """One blog can have many posts
       and if they try to delete the entire blog,
       then this logic is prohibited
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(PersonalBlog, on_delete=models.PROTECT, related_name='posts')

    def __str__(self):
        return f'{self.title}-->{self.blog.title}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.id)])


class Follower(models.Model):
    """One user can have many
     subscriptions to his blog
     and can subscribe to other blog
     """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='author')
    blog = models.ManyToManyField(PersonalBlog, verbose_name='blog')

    def __str__(self):
        return f'{self.user.username}'


class PostsRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts_read')
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}-->{self.post.title}-->{self.is_read}'


@receiver(post_save, sender=Post)
def save_post(sender, instance, **kwargs):
    transaction.on_commit(lambda: send_notification_to_followers_task.delay(10, instance.id))


