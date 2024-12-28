# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('select_topic/', views.select_topic, name='select_topic'),
 
     


   # Main quiz based on topic
    path('quiz/<int:topic_id>/', views.main_quiz, name='main_quiz'),

    # Reattempt quiz based on subtopic
    path('reattempt_quiz/<int:sub_topic_id>/', views.reattempt_quiz, name='reattempt_quiz'),
    
    

    path('result/<int:result_id>/', views.result, name='result'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]
