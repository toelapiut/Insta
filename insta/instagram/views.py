from django.shortcuts import render,redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Tag, Post, Follow, Comment, Like
from .forms import *
from wsgiref.util import FileWrapper
import mimetypes
from django.conf import settings
import os

# Create your views here.
@login_required(login_url='/accounts/register')
def timeline(request):
    '''
    View function to display the timeline page for an authenticated logged in user
    '''
    current_user = request.user

    title = 'Home'

    following = Follow.get_following(current_user.id)

    posts = Post.get_posts()

    following_posts = []

    for follow in following:

        for post in posts:

            if follow.profile == post.profile:

                following_posts.append(post)

    return render(request, 'all-posts/timeline.html', {"title": title, "following": following, "user":current_user, "following_posts":following_posts})

def index(request):
    '''
    View function to display the timeline page for an authenticated logged in user
    '''
    current_user = request.user

    title='instagram'

    following = Follow.get_following(current_user.id)

    posts = Post.get_posts()

    following_posts = []

    for follow in following:

        for post in posts:

            if follow.profile == post.profile:

                following_posts.append(post)

    return render(request, 'index.html', {"title": title, "following": following, "user":current_user, "following_posts":following_posts})
