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
#from django.contrib import admin
from django.conf.urls import include, url
from server import views
import oauth2_provider.views as oauth2_views
from django.conf import settings
#from rest_framework_jwt.views import obtain_jwt_token

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        url(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
        url(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        url(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        url(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        url(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        url(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        url(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]


urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^user/list/', views.user_list),
    url(r'^user/create/', views.create_update_user),
    url(r'^sound/details/(?P<pk>[0-9]+)/$', views.sound_detail),
    url(r'^label/create', views.create_label),
    url(r'^sound/list/', views.sound_list),
    url(r'^label/random/', views.label_random),
    url(r'^label/predict', views.label_predict),
    url(r'^label/getLabel', views.getLabel),
    url(r'^label/getSound',views.getSound),
    #url(r'^api-token-auth/',obtain_jwt_token),
    url(r'fcm/', include('fcm.urls')),
    url(r'^noti/send', views.FCM),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # OAuth 2 endpoints:
    url(r'^o/', include(oauth2_endpoint_views, namespace="oauth2_provider")),
]
