from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.homepage,name="homepage"),
    path('instagram/', views.photos, name="instagram"),
    path('posted/',views.posted,name="posted"),
    path('profile/', views.myprofile, name='profile'),
    re_path(r'^image/(\d+)',views.imageid,name ='article'),
    re_path(r'^like/(\d+)', views.like, name='like'),
    re_path(r'^update/profile', views.updatemyprofile, name='update_profile'),
    re_path(r'^comments/(\d+)', views.comment, name='comment'),
    path('search/', views.search_user, name='search_results'),

    re_path(r'^follow/(\d+)', views.follow, name='follow'),
    re_path(r'^followers/', views.allfollowers, name='viewProfiles'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

