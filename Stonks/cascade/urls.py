from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('aboutUs', include('main.urls')),
    path('FAQ', include('main.urls')),
    path('init', include('main.urls')),
    path('info/<str:share_name>/', include('main.urls')),
]



