from django.contrib import admin
from django.urls import path
from website import views
urlpatterns = [
    path('',views.login, name="login"),
    path('create/',views.createAccount, name="create"),
    path('accueil/',views.index, name="accueil"),
    path('profile/<int:id>',views.profile, name="profile"),
    path('addtopic/',views.addtopic, name="addtopic"),
    path('categorie/<int:id>',views.categorie, name="categorie"),
    path('topic/<int:id>',views.topicDetail, name="topic"),
    path('AdminIndex/',views.AdminIndex, name="AdminIndex"),
    path('loginAdmin/',views.loginAdmin, name="loginAdmin"),
    path('ADDAdmin/',views.ADDAdmin, name="ADDAdmin"),
    path('AdminsList/',views.AdminsList, name="AdminsList"),
    path('AdminCreateCategory/',views.AdminCreateCategory, name="AdminCreateCategory"),
    path('AdminCategoryUpdate/<int:id>',views.AdminCategoryUpdate, name="AdminCategoryUpdate"),
    path('AdminReplies/',views.AdminReplies, name="AdminReplies"),
    path('postedTopic/',views.postedTopic, name="postedTopic"),
    path('AdminCategory/',views.AdminCategory, name="AdminCategory"),

]