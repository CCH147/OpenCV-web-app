from django.contrib import admin
from mysite import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path("", views.home),
    path("mysite/", views.home),
    path('admin/', admin.site.urls),
    path('mysite/index', views.index),
    path('mysite/chart2/',views.chart),
    path('mysite/our/',views.our),
    path('mysite/datasum/',views.datasum),
    path('mysite/Image', views.image_view, name="image_view"),
    path('mysite/webcam', views.index_webcam),
    path('web_camera', views.webcam, name="web_camera"),
    re_path(r'^media/(?P<path>.*)$',serve,{"document_root":settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

