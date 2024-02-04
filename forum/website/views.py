from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import PostMessage, Category, Users, Reply, Admins
from django.db.models import Count
from django.conf import settings
import os
import json 
from datetime import date
from django.contrib import messages
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import FormView, ListView
from django.core.mail import EmailMessage


def sendmails( email, name,password):
        my_subject = "Email du ForumItEcole"
        my_recepient = [email]
        html_message = render_to_string("email.html", context={"name": name,"password":password})
        plain_message = strip_tags(html_message)
        message = EmailMultiAlternatives(
            subject=my_subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=my_recepient
        )
        message.attach_alternative(html_message, "text/html")
        message.send(fail_silently=False)

# Create your views here.
def index(request):
    totcat= Category.objects.all().count()
    totpos= PostMessage.objects.all().count()
    totuser= Users.objects.all().count()
    # id_user = request.session.get('id')
    # user= Users.objects.get(pk=id_user)
    # categories = Category.objects.annotate(nombre_occurences=Count(Category.added_by))
    categories= Category.objects.all()
    auth= True
    if not request.session.get('id'):
        auth=False
    me= request.session.get('id')
    try:
         id= Users.objects.get(email=request.session.get("email"))
    except Users.DoesNotExist:
        id={"pseudo":"visiteur@visiteur.com"}
    return render(request,"index.html", context={"postmessage": PostMessage.objects.all(), "totcat":totcat, "totpos":totpos,"totuser":totuser ,"categories":categories,"id":id,"auth":auth,"me":me})

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
            sendmails(email=email,name=pseudo, password=password) #envoi du mail 
            new_user = Users(pseudo=pseudo, email=email, password=password, role=role, birthdate=birthdate, description=description, avatar=avatar)
            new_user.save()
            img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
            with open(img_path, 'wb') as img_file:
                for chunk in avatar.chunks():
                    img_file.write(chunk)
            return redirect('login')
       else:
            me= request.session.get('id')
            return render(request, "register.html",context={"categories":categories,"me":me})

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
    me= request.session.get('id')
    return render(request, "login.html",context={"categories":categories,"me":me} )

def logoutUser(request):
    del request.session['pseudo']
    del request.session['id']
    del request.session['email']
    del request.session['role']
    del request.session['avatar']
    del request.session['activated']
    # del request.session['birthdate']
    del request.session['description']
    return redirect("login")



def profile(request,id):
    ut= Users.objects.get(pk=id)
    totcat= Category.objects.all().count()
    totpos= PostMessage.objects.all().count()
    totuser= Users.objects.all().count()
    categories= Category.objects.all()
    auth= True
    if not request.session.get('id'):
        auth=False
    try:
        id= Users.objects.get(email=request.session.get("email"))
    except:
        pass
    me= request.session.get('id')
    return render(request, 'profile.html', context={"user":ut,"totcat":totcat, "totpos":totpos,"totuser":totuser ,"categories":categories,"auth":auth,"id":id,"me":me})


def addtopic(request):
   if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        question = request.POST.get('question')  
        id_user = request.session.get('id')
        user = Users.objects.get(pk=id_user)
        category = Category.objects.get(pk=category_id)
        avatar = request.FILES.get('avatar')  
        img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
        with open(img_path, 'wb') as img_file:
            for chunk in avatar.chunks():
                img_file.write(chunk)
        new_post = PostMessage(title=title, message=question, category=category, user=user, avatar=avatar)
        new_post.save()
        return redirect('accueil')
   else:
      category= Category.objects.all()
      auth= True
      if not request.session.get('id'):
         auth=False
      me= request.session.get('id')

      id= Users.objects.get(email=request.session.get("email"))

      return render(request, "create.html" , context={"category":category,"auth":auth,"id":id,"me":me})


def categorie(request,id):
    categorie= Category.objects.get(pk=id)
    posts= PostMessage.objects.filter(category=categorie)

    totcat= Category.objects.all().count()
    totpos= PostMessage.objects.all().count()
    totuser= Users.objects.all().count()
    # id_user = request.session.get('id')
    # user= Users.objects.get(pk=id_user)
    # categories = Category.objects.annotate(nombre_occurences=Count(Category.added_by))
    categories= Category.objects.all()
    auth= True
    if not request.session.get('id'):
         auth=False
    try:
         id= Users.objects.get(email=request.session.get("email"))
    except Users.DoesNotExist:
        id={"pseudo":"visiteur@visiteur.com"}
    me= request.session.get('id')
    return render(request, "catgorie.html", context={"posts":posts,"totcat":totcat, "totpos":totpos,"totuser":totuser ,"categories":categories,"id":id,"auth":auth,"me":me})

def topicDetail(request,id):
    try:
        post= PostMessage.objects.get(pk=id)    
        us= Users.objects.get(pk=post.user.pk)
        reply= Reply.objects.filter(post=post)
        categories= Category.objects.all()
        # taille=len(dict(categorie))
    except PostMessage.DoesNotExist:
        auth= True #verifier si l'utililsateur est authentifier
        if not request.session.get('id'):
            auth=False
        me= request.session.get('id')

        return render(request, 'topic.html', context={'postmesg':"","auth":auth,"me":me})
    # id= Users.objects.get(email=request.session.get("email"))
    try:
         auth= True #verifier si l'utililsateur est authentifier
         if not request.session.get('id'):
            auth=False
         me= request.session.get('id')

         id= Users.objects.get(email=request.session.get("email"))
    except Users.DoesNotExist:
        id={"pseudo":"visiteur@visiteur.com"}
    return render(request, 'topic.html', context={'postmesg':post, "reply": reply, "categories": categories, "id":id, "auth":auth,"me":me})

#  ce script gère l'ajout des reponses dans le forum
def AddReply(request,id):
     if request.method == "POST":
         reponse= request.POST.get("reply")
         user= Users.objects.get(pk=request.session.get('id'))
         posts= PostMessage.objects.get(pk=id)
         rep= Reply(description=reponse,user=user,post=posts)
         rep.save()
         auth= True
         me= request.session.get('id')
         if not request.session.get('id'):
                auth=False
         try:
            post= PostMessage.objects.get(pk=id)    
            reply= Reply.objects.filter(post=post)
            categories= Category.objects.all()
         except PostMessage.DoesNotExist:
            auth= True
            if not request.session.get('id'):
                auth=False
            me= request.session.get('id')

            id= Users.objects.get(email=request.session.get("email"))
            return render(request, 'topic.html', context={'postmesg':"", "auth":auth,"id":id,"me":me})
         id= Users.objects.get(email=request.session.get("email"))
         return render(request, 'topic.html', context={'postmesg':post, "reply": reply, "categories": categories, "id":id, "auth":auth,"me":me})




 #Gestion des routes des admins 
     

def AdminIndex(request):
    users= Users.objects.all()
    emailAd= request.session.get("Admin_pseudo")
    return render(request, "admin-panel/index.html" ,context={"users":users,"pseudo":emailAd})

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
     emailAd= request.session.get("Admin_pseudo")
     if request.method == 'POST':
        email = request.POST.get('email')
        pseudo = request.POST.get('pseudo')
        password = request.POST.get('password')
        avatar =  request.FILES.get('avatar') 
        description = request.POST.get('description') 
        role="Admin"
        activated=True
        sendmails(email=email,name=pseudo, password=password) #envoi du mail 
        img_path = os.path.join(settings.MEDIA_ROOT,avatar.name)
        with open(img_path, 'wb') as img_file:
                for chunk in avatar.chunks():
                    img_file.write(chunk)
        new_user = Users(pseudo=pseudo, email=email, password=password, role=role, birthdate="2022-12-31", description=description, avatar=avatar)
        new_user.save()
        new_admin= Admins(pseudo=pseudo, email=email, password=password, role=role,  description=description, avatar=avatar, activated=activated)
        new_admin.save()
        return redirect("loginAdmin")
     return render(request, "admin-panel/admins/create-admins.html", context={"pseudo":emailAd})


def AdminsList(request):
    emailAd= request.session.get("Admin_pseudo")
    adm= Admins.objects.all()
    return render(request, "admin-panel/admins/admins.html", context={"admin":adm,"pseudo":emailAd})

#Gestion des routes Des Categories 
# forum\templates\admin-panel\categories-admins
def AdminCreateCategory(request):
        emailAd= request.session.get("Admin_pseudo")
        if request.method == 'POST':
             name = request.POST.get('name') 
             description=request.POST.get('description')
             added= request.session.get('Admin_id')
             adm= Admins.objects.get(pk=added)
             cat = Category(title=name, description=description, added_by=adm)
             cat.save()
             return redirect('AdminCategory')
        return render(request, "admin-panel/categories-admins/create-category.html",context={"pseudo":emailAd})

def AdminCategory(request):
    emailAd= request.session.get("Admin_pseudo")
    cat= Category.objects.all()
    return render(request, "admin-panel/categories-admins/show-categories.html" , context={"category":cat,"pseudo":emailAd})

def AdminCategoryUpdate(request, id):
    emailAd= request.session.get("Admin_pseudo")
    return render(request, "admin-panel/categories-admins/update-category.html" , context={"pseudo":emailAd})

#for replies

def AdminReplies(request):
    emailAd= request.session.get("Admin_pseudo")
    rep= Reply.objects.all()
    return render(request,"admin-panel/replies-admins/show-replies.html", context={"reply":rep,"pseudo":emailAd})
#for posted topic
def postedTopic(request):
    posts= PostMessage.objects.all()
    pseudo= request.session.get("Admin_pseudo")
    return render(request,"admin-panel/topics-admins/show-topics.html" , context={"posts":posts,"pseudo":pseudo})




#operations côté Admin (suppression , mise à jour)

#les catgories
def SupprimerCategorie(request,id):
    cat = Category.objects.get(pk=id).delete()
    return redirect("AdminCategory")

def MAJCategorie(request, id):
    emailAd= request.session.get("Admin_pseudo")
    cat = Category.objects.get(pk=id)
    if request.method == 'POST':
        name = request.POST.get('name') 
        description = request.POST.get('description')
        added = request.session.get('Admin_id')
        adm = Admins.objects.get(pk=added)

        # Mettre à jour les champs de l'objet cat avec les nouvelles valeurs
        cat.title = name
        cat.description = description
        cat.added_by = adm
        cat.save()  # Enregistrer les modifications dans la base de données
        return redirect("AdminCategory")
    return render(request, "admin-panel/categories-admins/update-category.html", context={"cat": cat,"pseudo":emailAd})


#fonction pour fermer un sujet
def FermerSujet(request, id):
    emailAd= request.session.get("Admin_pseudo")
    message= PostMessage.objects.get(pk=id)
    message.closes=True
    message.save()
    return redirect("postedTopic")



def logoutAdmin(request):
    emailAd= request.session.get("Admin_pseudo")
    keys_to_delete = ['Admin_pseudo', 'Admin_id', 'Admin_email', 'Admin_role', 'Admin_avatar', 'Admin_activated', 'Admin_description']
    for key in keys_to_delete:
        if key in request.session:
            del request.session[key]
    return redirect("loginAdmin")



def personalProfile(request,id):
    ut= Users.objects.get(pk=id)
    totcat= Category.objects.all().count()
    totuser= Users.objects.all().count()
    categories= Category.objects.all()
    auth= True
    if not request.session.get('id'):
        auth=False
    
    id= Users.objects.get(email=request.session.get("email"))
    post=PostMessage.objects.filter(user=id)
    totpos= PostMessage.objects.filter(user=id).count()
    totrep=Reply.objects.filter(user=id).count()
    me= request.session.get('id')
    return render(request, 'myprofile.html', context={"postmessage":post,"user":ut,"totcat":totcat, "totpos":totpos,"totuser":totuser ,"categories":categories,"auth":auth,"id":id, "totrep":totrep,"me":me})


def deletepost(request,id):
    post= PostMessage.objects.get(pk=id)
    post.delete()
    ut= Users.objects.get(pk=request.session.get('id'))
    totcat= Category.objects.all().count()
    totuser= Users.objects.all().count()
    categories= Category.objects.all()
    auth= True
    if not request.session.get('id'):
        auth=False
    
    id= Users.objects.get(email=request.session.get("email"))
    post=PostMessage.objects.filter(user=id)
    totpos= PostMessage.objects.filter(user=id).count()
    totrep=Reply.objects.filter(user=id).count()
    me= request.session.get('id')

    return render(request, 'myprofile.html', context={"postmessage":post,"user":ut,"totcat":totcat, "totpos":totpos,"totuser":totuser ,"categories":categories,"auth":auth,"id":id, "totrep":totrep,"me":me})


def editPost(request, id):
      post= PostMessage.objects.get(pk=id)
      if request.method == 'POST':
            title = request.POST.get('title') 
            cat = request.POST.get('category')
            cats= Category.objects.get(pk=cat)
            question = request.POST.get('question')
            post.title=title
            post.category=cats
            post.message=question
            post.save()
      category= Category.objects.all()
      post= PostMessage.objects.get(pk=id)
      auth= True
      if not request.session.get('id'):
         auth=False
      me= request.session.get('id')

      id= Users.objects.get(email=request.session.get("email"))
      return render(request, "editpost.html" , context={"category":category,"auth":auth,"id":id, "post":post,"me":me})


def deleteUser(request, id):
    ut= Users.objects.get(pk=id)
    ut.delete()
    return redirect("AdminIndex")