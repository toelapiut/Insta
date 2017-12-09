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
def index(request):

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

@login_required(login_url='/accounts/register')
def profile(request,id):

    current_user = request.user

    try:

        profile = Profile.objects.get(user=current_user.id)

        title = f'{current_user.username}\'s'

        posts = Post.objects.filter(user=current_user.id)

        return render(request, 'all-temps/profile.html', {"title":title,"current_user":current_user,"posts":posts})

    except DoesNotExists:
        raise Http404()

@login_required(login_url='/accounts/register')
def post(request):
  
    current_user = request.user

    current_profile = current_user.profile

    if request.method == 'POST':

        form = NewsPostForm(request.POST, request.FILES)

        if form.is_valid:

            post = form.save(commit=False)

            post.user = current_user

            post.profile = current_profile

            post.save()

            return redirect(profile, current_user.id)

    else:

        form = NewsPostForm()

    title = 'Create Post'

    return render(request,'all-temps/post.html', {"form":form})


@login_required(login_url='/accounts/register')
def look_up(request,id):

    current_user = request.user

    current_user_profile = current_user.profile

    profiles = Profile.get_other_profiles(current_user.id)

    following = Follow.objects.filter(user=current_user)

    following_profile_list = []

    for follow in following:

        following_profile_list.append(follow.profile)

    profiles_list = []

    for profile in profiles:

        if profile not in following_profile_list:

            profiles_list.append(profile)

    title = f'{current_user.username}'

    return render(request,'all-temps/look_up.html',{"title":title,"profiles":profiles_list})

@login_required(login_url='/accounts/register')
def follow(request,id):

    current_user = request.user

    follow_profile = Profile.objects.get(id=id)

    following = Follow(user=current_user, profile=follow_profile)

    following.save()

    return redirect(timeline)