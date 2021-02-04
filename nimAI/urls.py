from django.urls import path

from . import views

app_name = 'nimAI'

urlpatterns = [
    path('', views.index, name='index'),
    path('reset/', views.reset, name='reset'),
    path('train/', views.show_training_options, name='train'),
    path('play/', views.train_and_show_board, name='nim'),
    path('ai_move/', views.send_ai_move, name='ai_move'),
]
