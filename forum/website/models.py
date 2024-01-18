from django.db import models

class Users(models.Model):
    pseudo = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)  # Utilisation de CharField pour le mot de passe
    role = models.CharField(max_length=20, default="User")  # Limiter la longueur du rôle
    avatar = models.ImageField( null=True, blank=True, upload_to='img/')  # Ajout d'un champ pour l'avatar
    activated = models.BooleanField(default=True)  # Par défaut, l'utilisateur n'est pas activé
    birthdate= models.DateField(null=False)
    description= models.TextField(null=False, default='JE suis un membre anonyme du forum')


class Admins(models.Model):
    pseudo = models.CharField(max_length=50, unique=True)  # Utilisation de CharField pour le pseudo
    email = models.EmailField()
    password = models.CharField(max_length=100)  # Utilisation de CharField pour le mot de passe
    role = models.CharField(max_length=20, default="Admin")  # Limiter la longueur du rôle
    avatar = models.ImageField(null=True, blank=True, upload_to='img/')  # Ajout d'un champ pour l'avatar
    activated = models.BooleanField(default=True)  # Par défaut, l'administrateur n'est pas activé
    description= models.TextField(null=False, default='JE suis un membre anonyme du forum') 

class Category(models.Model):
    title = models.CharField(max_length=100)  # Augmentation de la longueur du titre
    description = models.TextField()
    added_by = models.ForeignKey(Admins, on_delete=models.CASCADE)  # Renommage du champ addedBy en snake_case

class PostMessage(models.Model):
    title = models.CharField(max_length=100)  # Augmentation de la longueur du titre
    message = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)  # Utilisation de DateTimeField pour la date et l'heure de publication
    closes = models.BooleanField(default=False)  # Par défaut, le message n'est pas clos
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Correction du nom du champ Category en minuscules
    user= models.ForeignKey(Users, on_delete= models.CASCADE)
 

class Reply(models.Model):
    description= models.TextField(max_length=1000)
    user= models.ForeignKey(Users, on_delete=models.CASCADE)
    post= models.ForeignKey(PostMessage, on_delete= models.CASCADE)
    