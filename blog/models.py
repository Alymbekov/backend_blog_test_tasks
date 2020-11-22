from django.db import models
from django.contrib.auth import get_user_model

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


class Follower(models.Model):
    """One user can have many
     subscriptions to his blog
     and can subscribe to other blogs
     """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='author')
    blog = models.ManyToManyField(PersonalBlog, verbose_name='blogs')

    def __str__(self):
        return f'{self.user.username}'



#TODO add signals to send message notifications




