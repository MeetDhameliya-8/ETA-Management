from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# Create your models here.

ROLE_CHOICES = [

    ('NJ','NewJoine'),
    ('Int','Intern'),
    ('Emp','Employee'),
    ('HR','HR'),
    ('MG','Manager'),
    ('OWN','Owner'),

    ]

Experience = [
    ('1Y','1 Years'),
    ('2Y','2 Years'),
    ('3Y','3 Years'),
    ('4Y','4 Years'),
    ('5Y','4 Years'),
    ('6Y','4 Years'),
    ('7Y+','7 Years'),
]

class UserManager(BaseUserManager):
    def create_user(self, email,phone, password=None):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email,
                          phone=phone)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,phone,password=None):

        user = self.create_user(
            email=email,
            phone=phone,
            password=password
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save(using = self._db)

        return user






class User(AbstractBaseUser,PermissionsMixin):



    email = models.CharField(verbose_name='Email Address',max_length=60,unique=True)
    first_name = models.CharField(max_length=50,blank=False,null=False)
    last_name = models.CharField(max_length=50,blank=False,null=False)
    phone = models.CharField(max_length=18,unique=True)
    passwd = models.CharField(max_length=80,null=False,blank=False)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,blank=False,null=False)
    Experience = models.CharField(verbose_name='Experience',choices=Experience)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_NewJoine = models.BooleanField(default=False)
    is_Intern = models.BooleanField(default=False)
    is_Employee = models.BooleanField(default=False)
    is_HR = models.BooleanField(default=False)
    is_Manager = models.BooleanField(default=False)
    is_Owner = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
         


    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["phone"]

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    
   

class NewJoineProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='NewjJoine')
    FullName = models.CharField(max_length=250, blank=False,null=False)
    
    Resume = models.FileField(upload_to='Profile/Resumes/', null=False, blank=False)
    AdharCard = models.ImageField(upload_to='Profile/AdharCard/', null=False,blank=False)
    panCard = models.ImageField(upload_to='Profile/PanCard/', null=False,blank=False)
    Check = models.ImageField(upload_to='Profile/Checks/',null=False,blank=False)
    SalarySlip = models.FileField(upload_to='Profile/SalarySlips/',null=True,blank=True)

    Address = models.CharField(max_length=200, null=False,blank=False)
    skills = ArrayField(models.CharField(max_length=50), blank=False, null=False, default=list)
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)  


class InternProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Intern')
    

