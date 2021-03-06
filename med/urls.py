"""med URL Configuration

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

from django.contrib import admin
from django.conf.urls import include, url
from medapi import views
#from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^medicine',views.search),
    url(r'^store$',views.store),
    url(r'^manufacturer',views.manufacture),
    url(r'^banned', views.banned),
    url(r'^lic', views.Lic),
    url(r'^store_med', views.store_med),
    url(r'^$',views.index),

]
#urlpatterns =format_suffix_patterns(urlpatterns)
