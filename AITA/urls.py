from django.urls import path

from . import views

app_name = 'AITA'

urlpatterns = [
    # ex: /AITA/
    path('', views.landing_page, name='landing'),
    path('intro/', views.intro, name='intro'),
    path('post/', views.show_post, name='post'),
]
