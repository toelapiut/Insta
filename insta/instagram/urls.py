from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url( r'^$', views.index, name="timeline"),
    url( r'^post', views.new_post, name="new-post"),
    url( r'^profile/(\d+)', views.profile, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
