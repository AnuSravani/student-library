from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta

import string
import random

class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)
    #used in issue book
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id



def generate_accession_number(length=8):
    characters = string.ascii_uppercase + string.digits
    uid = ''.join(random.choice(characters) for _ in range(length))
    return uid

class Book(models.Model):
    catchoice= [
        ('Education', 'Education'),
        ('Entertainment', 'Entertainment'),
        ('Comics', 'Comics'),
        ('Biography', 'Biographie'),
        ('History', 'History'),
        ('Romantic','Romantic'),
        ('Manipulation','Manipulation'),
        ('Fantacy','Fantacy'),

        ]
    name=models.CharField(max_length=30)
    image=models.ImageField(upload_to="images",null="True")
    isbn=models.PositiveIntegerField()
    author=models.CharField(max_length=40)
    description=models.TextField(null=True)
    category=models.CharField(max_length=30,choices=catchoice,default='Education')
    borrowsatus=models.BooleanField(default=False,null=True)
    published_year=models.TextField(null=True)
    quantity=models.TextField(null=True)
    accession_number =models.CharField(max_length=8, unique=True, blank=True, null=True)   

    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    enrollment=models.CharField(max_length=30)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self):
        return self.enrollment



class Userlibrarymodel(models.Model):
    first_name=models.TextField()
    last_name=models.TextField()
    email=models.EmailField()
    password=models.TextField()



def generate_transId(length=8):
    characters = string.ascii_uppercase + string.digits
    uid = ''.join(random.choice(characters) for _ in range(length))
    return uid
def get_expiry():
    return datetime.today() + timedelta(days=15)
class Transactionmodel(models.Model):
    trans_id=models.CharField(max_length=8, unique=True, blank=True, null=True)   
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    member=models.ForeignKey(Userlibrarymodel,on_delete=models.CASCADE)
    issuedate=models.DateField(auto_now=True)
    duedate=models.DateField(default=get_expiry)
    returndate=models.DateField(null=True)
    bookname=models.TextField()
    email=models.EmailField(null=True)
    bookstatus=models.BooleanField(null=True)
    def save(self, *args, **kwargs):
        if not self.trans_id:  # Only generate a new ID if it doesn't exist
            self.trans_id = generate_transId()
        super(Transactionmodel, self).save(*args, **kwargs)