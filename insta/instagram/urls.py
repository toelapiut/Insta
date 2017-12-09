from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url( r'^$', views.index, name="timeline"),
    url( r'^post', views.post, name="post"),
    url( r'^profile/(\d+)', views.profile, name="profile"),
    url( r'^comment(\d+)', views.comment, name="comment" ),
    url( r'^following/(\d+)', views.follow, name="follow"),
    url( r'^look_up/(\d+)', views.look_up, name="look-up"),
]

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
