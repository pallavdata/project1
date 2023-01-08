from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import FileExtensionValidator
from datetime import date
from uuid import uuid4
# Create your models here.

class MyManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("User must have an eamil address")
        if not username:
            raise ValueError("User must have an username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Login_Accounts(AbstractBaseUser):
    username = models.CharField(max_length=30,unique=True)
    email = models.EmailField(verbose_name="email",max_length=255,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login",auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=16,default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyManager()

    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,perm,obj=None):
        return True
    
class Job(models.Model):
    id = models.UUIDField(auto_created=True,primary_key = True,default = uuid4,editable = False,unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=200)
    salary = models.FloatField()
    description = models.TextField(max_length=400)
    experience = models.CharField(max_length=100)
    location = models.JSONField()
    skills = models.JSONField()
    creation_date = models.CharField(max_length=30)
    # def __str__(self):
    #     return f'title: {self.title}'

    
class Mcq(models.Model):
    id = models.UUIDField(auto_created =True,primary_key = True,default = uuid4,editable = False,unique=True)
    jobid = models.ForeignKey(Job,on_delete = models.CASCADE)
    question = models.CharField(max_length=1200)
    answer = models.CharField(max_length=240)
    option2 = models.CharField(max_length=240)
    option3 = models.CharField(max_length=240)
    option4 = models.CharField(max_length=240)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return f"{self.question} Answer - {self.answer}"



class Apply(models.Model):
    id = models.UUIDField(auto_created=True,primary_key = True,default = uuid4,editable = False,unique=True)
    jobid = models.ForeignKey(Job,on_delete = models.CASCADE)
    f_name = models.CharField(max_length=64,default="")
    l_name = models.CharField(max_length=64,default="")
    gender = models.CharField(max_length=6,default="")
    email_id = models.EmailField(default="",unique=True)
    edu_year = models.CharField(max_length=4,default="")
    skill = models.JSONField()
    edu_collage_name = models.CharField(max_length=120,default="")
    edu_marks = models.CharField(max_length=9,default="",blank=True)
    internship = models.CharField(max_length=2000,default="",blank=True)
    img = models.ImageField(upload_to='img/'+str(date.today()),null=True, blank=True,default="")
    resume = models.FileField(upload_to='resume/'+str(date.today()), validators=[FileExtensionValidator( ['pdf'] ) ],default="")
    apply_date = models.CharField(max_length=30)
    hired = models.IntegerField(default=0)
    interview = models.IntegerField(default=0)
    assignment = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    # def __str__(self):
    #     return f'name: {self.f_name} {self.l_name} and edu_collage_name: {self.edu_collage_name}'
class Apply_candidate(models.Model):
    customid = models.UUIDField(auto_created=True,default = uuid4,editable = False,unique=True)
    Applyid = models.ForeignKey(Apply,on_delete = models.CASCADE)

class AssignmentTemp(models.Model):
    type = models.CharField(max_length=120, unique=True)
    text = models.CharField(max_length=6010)

class InterviewTemp(models.Model):
    text = models.CharField(max_length=6010)

class EventDb(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    meetUrl = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
# from django.contrib.staticfiles.storage import staticfiles_storage
# class zip(models.Model):
#     zip = models.FileField(upload_to=f'{staticfiles_storage.url(path)}/'+str(date.today()), validators=[FileExtensionValidator( ['pdf'] ) ],default="")

class role(models.Model):
    role = models.CharField(max_length=200)

class skill(models.Model):
    skill = models.CharField(max_length=200)