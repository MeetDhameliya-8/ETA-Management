from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
import uuid
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
    ('5Y','5 Years'),
    ('6Y','6 Years'),
    ('7Y+','7 Years'),
]

TECH = [
    ('BD','backend'),
    ('FD','frontend'),
    ('FS','fullstack')
]

ASSIGNER = [

    ('MG','Manager'),
    ('EP','Employee'),
    ('OWN','Owner'),
    ('HR','HR')

]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None):

        user = self.create_user(
            email=email,
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
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,blank=False,null=False)
    technology = models.CharField(verbose_name='Technology',choices=TECH, blank=True,null=False)
    Experience = models.CharField(verbose_name='Experience',choices=Experience, default='1Y')
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

    REQUIRED_FIELDS = ["password"]

    @property
    def is_newjoine(self):
        return self.role == 'NewJoinee'

    @property
    def is_intern(self):
        return self.role == 'Intern'

    @property
    def is_employee(self):
        return self.role == 'Employee'

    @property
    def is_manager(self):
        return self.role == 'Manager'

    @property
    def is_hr(self):
        return self.role == 'HR'

    @property
    def is_owner(self):
        return self.role == 'Owner'

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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='newjoine_profile')
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='intern_profile')
    FullName = models.CharField(max_length=250, blank=False,null=False)
    skills = ArrayField(models.CharField(max_length=50), blank=False, null=False, default=list)
    Task = models.CharField(max_length=200,null=True)
    Assigner = models.CharField(max_length=60,blank=False,null=False,choices=ASSIGNER)  
    next_Intrest = ArrayField(models.CharField(max_length=50),blank=False, null=False, default=list)    
    Part_of_Project = models.CharField(max_length=20,null=False,blank=False)    
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)    

class EmployeeProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    salary = models.DecimalField(null=False,blank=False,max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=25,unique=True,blank=False,null=False)
    Bio = models.FileField(upload_to='Profile/BioFile',blank=False,null=False,default='PENDING')
    Project = models.CharField(max_length=90,blank=False,null=False)
    Project_AssignedDate = models.DateTimeField(blank=False,null=False)
    Assigner = models.CharField(max_length=60,blank=False,null=False,choices=ASSIGNER)
    TeamMembers = ArrayField(models.CharField(max_length=50), blank=False, null=False, default=list)
    skills = ArrayField(models.CharField(max_length=50), blank=False, null=False, default=list)
    PreviousCompany = models.FileField(upload_to='Profile/PreCom/',default='Null')
    DayUpdate =  models.CharField(max_length=300,blank=False,null=False,default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)   
    updated_at = models.DateTimeField(auto_now=True)  



class HrProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hr_profile')
    FullName = models.CharField(max_length=250, blank=False,null=False)
    department = models.CharField(max_length=100, blank=False,null=False)              
    position = models.CharField(max_length=100, blank=False,null=False)                
    contact_number = models.CharField(max_length=15, blank=False,null=False, unique=True)
    candidates_managed = models.PositiveIntegerField(default=0)                                 
    employees_under = models.PositiveIntegerField(default=0)  # number of employees handled
    interviews_scheduled = models.PositiveIntegerField(default=0)               
    can_hire = models.BooleanField(default=True)               
    max_open_positions = models.IntegerField(default=1)         
    current_openings = models.IntegerField(default=0)           
    can_assign_to_manager = models.BooleanField(default=True)
    can_approve_leave = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


class ManagerProfile(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    FullName = models.CharField(max_length=250, blank=False,null=False)
    department = models.CharField(max_length=100, blank=False,null=False)
    Team = models.CharField(max_length=50,null=False,default='Pending',blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

     


    

class OwnerProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    FullName = models.CharField(max_length=250, blank=False,null=False)
    Experience = models.CharField(max_length=600, blank=False, null=False)
    skills = ArrayField(models.CharField(max_length=50), blank=False, null=False, default=list) 
    Projects_Completed = models.IntegerField(blank=False,null=False,default='10+')


     