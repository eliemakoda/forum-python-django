from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import PostMessage, Category, Users, Reply, Admins
from django.db.models import Count
from django.conf import settings
import os
import json 
from datetime import date
from django.contrib import messages
# Create your views here.
def index(request):
    totcat= Category.objects.all().count()
    totpos= PostMessage.objects.all().count()
    totuser= Users.objects.all().count()
    id_user = request.session.get('id')
    user= Users.objects.get(pk=id_user)
    # categories = Category.objects.annotate(nombre_occurences=Count(Category.added_by))
    categories= Category.objects.all()

    id= Users.objects.get(email=request.session.get("email"))
    return render(request,"index.html", context={"postmessage": PostMessage.objects.all(), "totcat":totcat, "totpos":totpos,"totuser":totuser ,"categories":categories,"id":id})

def createAccount(request):
       categories= Category.objects.all()
       if request.method == 'POST':
            pseudo = request.POST.get('pseudo')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role','User')
            birthdate = request.POST.get('bithday')
            description = request.POST.get('about')
            avatar = request.FILES.get('avatar')  
            new_user = Users(pseudo=pseudo, email=email, password=password, role=role, birthdate=birthdate, description=description, avatar=avatar)
            new_user.save()
            img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
            with open(img_path, 'wb') as img_file:
                for chunk in avatar.chunks():
                    img_file.write(chunk)
            return redirect('login')
       else:
            return render(request, "register.html",context={"categories":categories})

def login (request):
    categories= Category.objects.all()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Vérifier si l'utilisateur existe dans la base de données
        try:
            user = Users.objects.get(email=email, password=password)
        except Users.DoesNotExist:
            messages.error(request, 'Email ou mot de passe incorrect')
            return redirect('login')
        request.session['pseudo'] = user.pseudo
        request.session['id'] = user.pk
        request.session['email'] = user.email
        request.session['role'] = user.role
        request.session['avatar'] = user.avatar.url if user.avatar else None
        request.session['activated'] = user.activated
        # request.session['birthdate'] = user.birthdate
        request.session['description'] = user.description
        return redirect('accueil')
    return render(request, "login.html",context={"categories":categories} )




def profile(request,id):
    ut= Users.objects.get(pk=id)
    return render(request, 'profile.html', context={"user":ut})


def addtopic(request):
   if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        question = request.POST.get('question')  
        id_user = request.session.get('id')
        user = Users.objects.get(pk=id_user)
        category = Category.objects.get(pk=category_id)
        new_post = PostMessage(title=title, message=question, category=category, user=user)
        new_post.save()
        
        return redirect('accueil')
   else:
      category= Category.objects.all()
      return render(request, "create.html" , context={"category":category})


def categorie(request,id):
    categorie= Category.objects.get(pk=id)
    posts= PostMessage.objects.filter(category=categorie)

    totcat= Category.objects.all().count()
    totpos= PostMessage.objects.all().count()
    totuser= Users.objects.all().count()
    id_user = request.session.get('id')
    user= Users.objects.get(pk=id_user)
    # categories = Category.objects.annotate(nombre_occurences=Count(Category.added_by))
    categories= Category.objects.all()
    return render(request, "catgorie.html", context={"posts":posts,"totcat":totcat, "totpos":totpos,"totuser":totuser ,"categories":categories,"id":id})

def topicDetail(request,id):
    try:
        post= PostMessage.objects.get(pk=id)    
        us= Users.objects.get(pk=post.user.pk)
        reply= Reply.objects.filter(post=post)
        categories= Category.objects.all()
    except PostMessage.DoesNotExist:
        return render(request, 'topic.html', context={'postmesg':""})
    return render(request, 'topic.html', context={'postmesg':post, "reply": reply, "categories": categories})
 




 #Gestion des routes des admins 
def AdminIndex(request):
    return render(request, "admin-panel/index.html")

def loginAdmin(request):
     if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            # Vérifier si l'utilisateur existe dans la base de données
            try:
                user = Admins.objects.get(email=email, password=password)
                request.session['Admin_pseudo'] = user.pseudo
                request.session['Admin_id'] = user.pk
                request.session['Admin_email'] = user.email
                request.session['Admin_role'] = user.role
                request.session['Admin_avatar'] = user.avatar.url if user.avatar else None
                request.session['Admin_activated'] = user.activated
                # request.session['birthdate'] = user.birthdate
                request.session['Admin_description'] = user.description
                return redirect('AdminIndex')
            except Admins.DoesNotExist:
                # messages.error(request, 'Email ou mot de passe incorrect')
                return redirect('loginAdmin')

     return render(request, "admin-panel/admins/login-admins.html")


def ADDAdmin(request):
 
     if request.method == 'POST':
        email = request.POST.get('email')
        pseudo = request.POST.get('pseudo')
        password = request.POST.get('password')
        avatar =  request.FILES.get('avatar') 
        description = request.POST.get('description') 
        role="Admin"
        activated=True
        img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
        with open(img_path, 'wb') as img_file:
                for chunk in avatar.chunks():
                    img_file.write(chunk)
        new_user = Users(pseudo=pseudo, email=email, password=password, role=role, birthdate="2022-12-31", description=description, avatar=avatar)
        new_user.save()
        new_admin= Admins(pseudo=pseudo, email=email, password=password, role=role,  description=description, avatar=avatar, activated=activated)
        new_admin.save()
        return redirect("loginAdmin")
     return render(request, "admin-panel/admins/create-admins.html")


def AdminsList(request):
    adm= Admins.objects.all()
    return render(request, "admin-panel/admins/admins.html", context={"admin":adm})

#Gestion des routes Des Categories 
# forum\templates\admin-panel\categories-admins
def AdminCreateCategory(request):
        if request.method == 'POST':
             name = request.POST.get('name') 
             description=request.POST.get('description')
             added= request.session.get('Admin_id')
             adm= Admins.objects.get(pk=added)
             cat = Category(title=name, description=description, added_by=adm)
             cat.save()
             return redirect('AdminCategory')
        return render(request, "admin-panel/categories-admins/create-category.html")

def AdminCategory(request):
    cat= Category.objects.all()
    return render(request, "admin-panel/categories-admins/show-categories.html" , context={"category":cat})

def AdminCategoryUpdate(request, id):
    return render(request, "admin-panel/categories-admins/update-category.html")

#for replies

def AdminReplies(request):
    rep= Reply.objects.all()
    return render(request,"admin-panel/replies-admins/show-replies.html", context={"reply":rep})
#for posted topic
def postedTopic(request):
    posts= PostMessage.objects.all()
    return render(request,"admin-panel/topics-admins/show-topics.html" , context={"posts":posts})