"""sound_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from server import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/list/', views.user_list),
    url(r'^user/create/', views.create_update_user),
    url(r'^sound/details/(?P<pk>[0-9]+)/$', views.sound_detail),
    url(r'^label/create', views.create_label),
    url(r'^sound/list/', views.sound_list),
    url(r'^label/random/', views.label_random),
    url(r'^label/predict', views.label_predict),
]
