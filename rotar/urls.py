"""goparweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path,include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap

from Apps.home.sitemap import ProductosSitemap, Sitemap


sitemaps = {
    'site': Sitemap(['home_app:inicio']),
    'productos': ProductosSitemap
}

urlpatterns_sitemap = [
    path('sitemap.xml', sitemap,{'sitemaps':sitemaps},
    name='django.contrib.sitemaps.views,sitemap')

]

urlpatterns_main = [
    path('admin/', admin.site.urls),
    re_path('',include('Apps.home.urls')),
    re_path('',include('Apps.publicaciones.urls')),
    re_path('',include('Apps.producto.urls')),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urlpatterns_main + urlpatterns_sitemap