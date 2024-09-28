from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.core.mail import send_mail
from django.utils import timezone 
#from librarymanagement.settings import EMAIL_HOST_USER


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')



def adminsignup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('adminlogin')
    return render(request,'library/adminsignup.html',{'form':form})


def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)

            f2.user=user
            user2=f2.save()    

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)


def userlogin(request):
    if request.method == "POST":
        data=models.Userlibrarymodel.objects.get(first_name=request.POST["first_name"])
        return redirect()



def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    else:
        return render(request,'library/studentafterlogin.html')



def addbook_view(request):
    #now it is empty book form for sending to html
    form=forms.BookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})







def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'library/bookissued.html')
    return render(request,'library/issuebook.html',{'form':form})



def viewissuedbook_view(request):
    issuedbooks=models.Transactionmodel.objects.all()
    print(issuedbooks)
    # li=[]
    # for ib in issuedbooks:
    #     issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
    #     expdate=str(ib.duedate.day)+'-'+str(ib.duedate.month)+'-'+str(ib.duedate.year)
    #     #fine calculation
    #     days=(date.today()-ib.issuedate)
    #     print(date.today())
    #     d=days.days
    #     fine=0
    #     if d>15:
    #         day=d-15
    #         fine=day*10
    if request.method =="POST":
        book_id = request.POST.get('book_id')
        
        transBook=models.Transactionmodel.objects.get(trans_id=book_id)
        transBook.bookstatus = True  
        transBook.returndate = timezone.now()  
        
        transBook.save()
        return redirect("/viewissuedbook")

    return render(request,'library/viewissuedbook.html',{'issuedbooks':issuedbooks})

def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})

def aboutus_view(request):
    return render(request,'library/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message, EMAIL_HOST_USER, ['wapka1503@gmail.com'], fail_silently = False)
            return render(request, 'library/contactussuccess.html')
    return render(request, 'library/contactus.html', {'form':sub})




def userview(request):
    if request.method == "POST":
        form=forms.userForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
    return render(request,'library/studentsignup.html')

def userlogin(request):
    if request.method  == "POST":
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            return redirect("allcategory")
    return render(request,"library/studentlogin.html")



def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'library/viewbook.html',{"data":books})

def category_view(request):
    books=models.Book.objects.all()
    return render(request,'library/categoryview.html',{'books':books})



def bookview(request, id):
    data = get_object_or_404(models.Book, id=id)

    if request.method == "POST":
        if not data.borrowsatus: 
            data.borrowsatus = True
            data.save()
            return redirect('bookview',id=id)  

    return render(request, "library/bookview.html", {'data': data})



def booktranaction(request):
    data=models.Transactionmodel.objects.all()
    return render(request,'library/viewissuedbook.html',{"data":data})

def viewedubook_view(request):
    if models.Book.objects.filter(category ="Education"):
        data1=models.Book.objects.filter(category ="Education")
        query = request.GET.get('q', '')  
        if query:
            data1 = models.Book.objects.filter(
                name__icontains=query
            ) | models.Book.objects.filter(
                author__icontains=query
            ) | models.Book.objects.filter(
                published_year__icontains=query
            )
        context = {
            "data1":data1,
            'query': query
        }
        return render(request, 'library/viewedubook.html',context)
    else:
        return render(request, 'library/viewedubook.html')


    

def viewbookromatic_view(request):
    if models.Book.objects.filter(category="Romantic"):
        data2=models.Book.objects.filter(category ="Romantic")
        query = request.GET.get('q', '')  
        if query:
            data2 = models.Book.objects.filter(
                name__icontains=query
            ) | models.Book.objects.filter(
                author__icontains=query
            ) | models.Book.objects.filter(
                published_year__icontains=query
            )
        context = {
            "data2":data2,
            'query': query
        }
        return render(request, 'library/romanticbooks.html', context)
    else:
        return render(request, 'library/romanticbooks.html')


def viewbookenter_view(request):
    if models.Book.objects.filter(category ="Entertainment"):
        data3=models.Book.objects.filter(category ="Entertainment")
        query = request.GET.get('q', '')  
        if query:
            data3 = models.Book.objects.filter(
                name__icontains=query
            ) | models.Book.objects.filter(
                author__icontains=query
            ) | models.Book.objects.filter(
                published_year__icontains=query
            )
        context = {
            "data3":data3,
            'query': query
        }
        return render(request, 'library/entertainmentbook.html',context) 
    else:
        return render(request, 'library/entertainmentbook.html') 
    


def viewbookcos_view(request):   
    if models.Book.objects.filter(category ="Comics"):
        data=models.Book.objects.filter(category ="Comics")
        query = request.GET.get('q', '')  
        if query:
            data = models.Book.objects.filter(
                name__icontains=query
            ) | models.Book.objects.filter(
                author__icontains=query
            ) | models.Book.objects.filter(
                published_year__icontains=query
            )
        context = {
            "data4":data,
            'query': query
        }
        return render(request, 'library/Comicsbook.html', context) 
    else:
        return render(request, 'library/Comicsbook.html') 


def viewbookbio_view(request):   
    if models.Book.objects.filter(category ="Biographie"):
        data=models.Book.objects.filter(category ="Biographie")
        query = request.GET.get('q', '')  
        if query:
            data = models.Book.objects.filter(
                name__icontains=query
            ) | models.Book.objects.filter(
                author__icontains=query
            ) | models.Book.objects.filter(
                published_year__icontains=query
            )
        context = {
            "data5":data,
            'query': query
        }
        return render(request,'library/Biographiebook.html', context)
    else:
        return render(request,'library/Biographiebook.html')

        

def viewbookhis_view(request):
    if models.Book.objects.filter(category ="History"):
        data=models.Book.objects.filter(category ="History")
        query = request.GET.get('q', '')  
        if query:
            data = models.Book.objects.filter(
                name__icontains=query
            ) | models.Book.objects.filter(
                author__icontains=query
            ) | models.Book.objects.filter(
                published_year__icontains=query
            )
        context = {
            "data6":data,
            'query': query
        }
        return render(request, 'library/Historybooks.html',context)
    else:
        return render(request, 'library/Historybooks.html')

        

def viewbookfatacy_view(request):
    if models.Book.objects.filter(category ="Fantacy"):
        data=models.Book.objects.filter(category ="Fantacy")
        query = request.GET.get('q', '')  
        if query:
            data = models.Book.objects.filter(
                name__icontains=query
            ) | models.Book.objects.filter(
                author__icontains=query
            ) | models.Book.objects.filter(
                published_year__icontains=query
            )
        context = {
            "data8":data,
            'query': query
        }
        return render(request, 'library/fantacybook.html',context)
    else:
        return render(request, 'library/fantacybook.html')


def viewbookmanipulate_view(request):
    if models.Book.objects.filter(category ="Manipulation"):
        data=models.Book.objects.filter(category ="Manipulation")
        query = request.GET.get('q', '')  
        if query:
            data = models.Book.objects.filter(
                name__icontains=query
            ) | models.Book.objects.filter(
                author__icontains=query
            ) | models.Book.objects.filter(
                published_year__icontains=query
            )
        context = {
            "data7":data,
            'query': query
        }
        return render(request, 'library/manipulationbook.html', context)
    else:
        return render(request, 'library/manipulationbook.html')


def booklistview(request):
    return render(request,'library/categoryview.html')


def logout_view(request):
    logout(request)
    return redirect('signin') 
