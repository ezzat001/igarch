"""ig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('logout',logoutview),
    path('unfollowers',unfollowers),
    path('dontfollowback',dontfollowuback),
    path('didntlikeyou',didntlikeany),
    path('toplikers',toplikers),
    path('privateuncovered',private_uncover),
    path('uncover=<str:target>', look_uncovered),
    path('toplikersearch', toplikersearch),
    path('toplikersof-<str:target>', toplikersof),
    path('whodidntlikesearch', whodidntlikethem),
    path('whodidntlike-<str:target>', whodidntliketarget),
    path('dontfollowbacksearch', dontfollowbacksearch),
    path('dontfollowback-<str:target>', dontfollowbacktarget),
    path('stalksomeone',stalktargetinsert),
    path('stalkdetails=<str:target>', stalk_details),
    #path('home', home_page),
    #path('test', templatetest),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
