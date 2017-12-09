from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum


# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)

    profile_pic = models.ImageField(upload_to="profile-pic/", blank=True)

    def __str__(self):

        return self.user.username

    @classmethod
    def get_profiles(cls):

        profiles = Profile.objects.all()

        return profiles

    @classmethod
    def get_other_profiles(cls,user_id):

        profiles = Profile.objects.all()

        other_profiles = []

        for profile in profiles:

            if profile.user.id != user_id:

                other_profiles.append(profile)

        return other_profiles

# Create Profile when creating a User
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Save Profile when saving a User
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Follow(models.Model):

    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    profile = models.ForeignKey(Profile,on_delete=models.DO_NOTHING,)

    def __str__(self):
        return self.user.username

    @classmethod
    def get_following(cls,user_id):

        following =  Follow.objects.filter(user=user_id).all()

        return following

class Tag(models.Model):
   
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    def save_tag(self):
       
        self.save()

    def delete_tag(self):
     
        self.delete()

    @classmethod
    def get_tags(cls):

        gotten_tags = Tag.objects.all()

        return gotten_tags

class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    post_date = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to="posts/")

    caption = models.TextField(blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:

        ordering = ['-post_date']

    @classmethod
    def get_posts(cls):

        posts = Post.objects.all()

        return posts

    @classmethod
    def get_profile_posts(cls,profile_id):

        profile_posts = Post.objects.filter(profile=profile_id).all()

        return profile_posts