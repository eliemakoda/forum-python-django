from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import PostMessage, Category, Users, Reply
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
    return render(request, "create.html")


def categorie(request,id):
    return render(request, "catgorie.html")

def topicDetail(request,id):
    try:
        post= PostMessage.objects.get(pk=id)    
        us= Users.objects.get(pk=post.user.pk)
        reply= Reply.objects.filter(user=us)
        categories= Category.objects.all()
    except PostMessage.DoesNotExist:
        return render(request, 'topic.html', context={'postmesg':""})
    return render(request, 'topic.html', context={'postmesg':post, "reply": reply, "categories": categorie})
 