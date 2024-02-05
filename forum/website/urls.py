from django.contrib import admin
from django.urls import path
from website import views
urlpatterns = [
    path('',views.index, name="accueil"),
    path('login/',views.login, name="login"),
    path('create/',views.createAccount, name="create"),
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
    path('AddReply/<int:id>',views.AddReply, name="AddReply"),
    path('logoutUser/',views.logoutUser, name="logoutUser"),
    path('SupprimerCategorie/<int:id>',views.SupprimerCategorie, name="SupprimerCategorie"),
    path('MAJCategorie/<int:id>',views.MAJCategorie, name="MAJCategorie"),
    path('FermerSujet/<int:id>',views.FermerSujet, name="FermerSujet"),
    path('logoutAdmin/',views.logoutAdmin, name="logoutAdmin"),
    path('personalProfile/<int:id>',views.personalProfile, name="personalProfile"),
    path('deletepost/<int:id>',views.deletepost, name="deletepost"),
    path('editPost/<int:id>',views.editPost, name="editPost"),
    path('deleteUser/<int:id>',views.deleteUser, name="deleteUser"),

]