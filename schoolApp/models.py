from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES=(
        ('Admin','Admin'),
        ('Teacher','Teacher'),
    )
    role=models.CharField(max_length=100,choices=ROLE_CHOICES,default='Teacher')


class TeacherModel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='teacher')
    subject=models.CharField(max_length=100)
    phone=models.CharField(max_length=30,blank=True,null=True)
    hire_date=models.DateField()
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.subject})"

class Student(models.Model):
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    grade = models.CharField(max_length=50)
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"