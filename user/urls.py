from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.login,name ='login'),
    path('register',views.register,name = 'register'),
    path('logout',views.logout, name='logout' ),
    path('college',views.college,name='college'),
    path('chatBot',views.chatBot,name='chatBot'),
    path('aiInterview',views.aiInterview,name = 'aiInterview'),
    path('expense',views.expense,name='expense'),
    path('studyplanner',views.studyplanner,name='studyplanner'),
    path('visa',views.visa,name='visa'),
    path('scholarship',views.scholarship,name='scholarship')
    
]
