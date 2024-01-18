from django.contrib import admin
from django.urls import path
from website import views
urlpatterns = [
    path('',views.index, name="accueil"),
    path('create/',views.createAccount, name="create"),
    path('login/',views.login, name="login"),
    path('profile/<int:id>',views.profile, name="profile"),
    path('addtopic/',views.addtopic, name="addtopic"),
    path('categorie/<int:id>',views.categorie, name="categorie"),
    path('topic/<int:id>',views.topicDetail, name="topic"),
]