from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.forms import Post,Comment
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required#used in function based views
from django.contrib.auth.mixins import LoginRequiredMixin#used in csb, a mixin is akin to decorators
from django.views.generic import (TemplateView,ListView,
                                    DetailView,CreateView,
                                    UpdateView,DeleteView)
from blog.models import Post,Comment
from blog.forms import PostForm, CommentForm
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    #Defining how to grab the list
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    #grab all the objects less than or equal to(lte) and then order them by decreasing order of date(most recent first)
    #  '-published_date' most recent first, 'published_date'- oldest first
    #__ separates field elements for field lookup, for more -https://docs.djangoproject.com/en/2.2/topics/db/queries/

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'#if not logged in go to this url
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    #When we are deleting a view we dont want the success_url to activate until we delete it, otherwise we will be jumping to other webpage
    #So we will reverse_lazy instead of reverse
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


###################
###################
@login_required
def add_comment_to_post(request,pk):#to add post we take request and pk to link comment to the post
    post = get_object_or_404(Post,pk=pk)#get object or 404 error page
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post#connect post to post object,
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
     comment = get_object_or_404(Comment,pk=pk)
     comment.approve()#calling the aprove method on model Comment
     return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)#we are saving comment.post.pk because after coment.delete() no key will be there

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)
