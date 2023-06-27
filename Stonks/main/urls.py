from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.info),
    path('aboutUs', views.aboutUsPage),
    path('FAQ', views.faqPage),
    path('init', views.init),
    path('info/<str:share_name>/', views.sharePage),

]
