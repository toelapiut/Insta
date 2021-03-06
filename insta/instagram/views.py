from django.shortcuts import render,redirect
from django.core.exceptions import ObjectDoesNotExist
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
def post(request):
  
    current_user = request.user

    current_profile = current_user.profile

    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)

        if form.is_valid:

            post = form.save(commit=False)

            post.user = current_user

            post.profile = current_profile

            post.save()

            return redirect(profile, current_user.id)

    else:

        form = PostForm()

    title = 'Create Post'

    return render(request,'all-temps/post.html', {"form":form})


@login_required(login_url='/accounts/register')
def profile(request,id):
    '''
    View function to display the profile of the logged in user when they click on the user icon
    '''
    current_user = request.user

    try:

        single_profile = Profile.objects.get(user=current_user.id)

        title = f'{current_user.username}\'s'

        posts = Post.objects.filter(user=current_user.id)

        return render(request, 'all-temps/profile.html', {"title":title,"current_user":current_user,"posts":posts})

    except ObjectDoesNotExist:
        raise Http404()


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

    return redirect(index)


@login_required(login_url='/accounts/register')
def comment(request,id):

    current_user = request.user

    current_post = Post.objects.get(id=id)

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid:

            comment = form.save(commit=False)

            comment.user = current_user

            comment.post = current_post

            comment.save()

            return redirect(post_look,current_post.id)

    else:

        form = CommentForm()

    title = f'Comment {current_post.user.username}'

    return render(request,'all-temps/comment.html', {"title":title,"form":form,"current_post":current_post})

@login_required(login_url='/accounts/register')
def like(request,id):

    current_user = request.user

    current_post = Post.objects.get(id=id)

    like = Like(user=current_user,post=current_post,likes_number=1)

    like.save()

    return redirect(post_look,current_post.id)

@login_required(login_url='/accounts/register')

def post_look(request,id):
    '''
    View function to display a single post, its comments and likes
    '''
    current_user = request.user
    try:
        current_post = Post.objects.get(id=id)

        title = f'{current_post.user.username}'
        comments = Comment.get_post_comments(id)

        likes = Like.num_likes(id)

        like = Like.objects.filter(post=id).filter(user=current_user)

    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'all-temps/post_look.html', {"title":title, "post":current_post,"comments":comments,"likes":likes,"like":like })

