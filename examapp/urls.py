from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('registration/', views.registration,name="registration"),
    path('login/', views.login,name="login"),
    path('dataset/', views.dataset,name="dataset"),
    path('training/', views.train,name="trainning"),
    path('questions/<str:email>',views.question,name="question"),
    path('stream/',views.livefe,name="livefeed" ),
    path('logout/',views.logout,name="logout"),
    path('score/', views.score,name='score'),
]