from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.DO_NOTHING)#only super user can Create new Post
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)#a post may be posted later

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)#grabing approved approve_comments

    def get_absolute_url(self):#this tells what to do once you created the Instance
    # it is telling that after creating post and hitting publication go to detail page
        return reverse('post_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.DO_NOTHING)#this 'comments' is same as defined in return self.comments.filter(approve_comment=True)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)#approved_commentm should be same as  mentioned in approve_comments function i.e -     return self.comments.filter(approve_comments=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')#we are sending to post_list u can send somewhere else also

    def __str__(self):
        return self.text
