"""librarymanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls') ),
    path('', views.home_view),

    path('adminclick', views.adminclick_view),
    # path('studentclick', views.studentclick_view),


    path('adminsignup', views.adminsignup_view),
    path('studentsignup', views.userview),
    path('adminlogin', LoginView.as_view(template_name='library/adminlogin.html')),
    path('studentlogin', LoginView.as_view(template_name='library/studentlogin.html'),name="login"),

    path('logout', LogoutView.as_view(template_name='library/index.html')),
    path('afterlogin', views.afterlogin_view),

    path('addbook', views.addbook_view),
    # path('viewbook', views.viewbook_view),
    path('issuebook', views.issuebook_view),
    path('viewissuedbook', views.viewissuedbook_view),
    path('viewstudent', views.viewstudent_view),
    path('viewissuedbookbystudent', views.viewissuedbookbystudent),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('viewbook_view',views.viewbook_view,name="viewbook"),
    path('category_view',views.category_view,name="categoryview"),
    path('login',views.userlogin,name="signin"),
    path('bookview/<id>',views.bookview,name="bookview"),
    path('viewbookedu_view',views.viewedubook_view,name="viewedubook"),
    path('viewbookromatic_view',views.viewbookromatic_view,name="viewbookromatic"),
    path('viewbookbio_view',views.viewbookbio_view,name="viewbookbio"),
    path('viewbookenter_view',views.viewbookenter_view,name="viewbookenter"),
    path('viewbookhis_view',views.viewbookhis_view,name="viewbookhis"),
    path('viewbookcos_view',views.viewbookcos_view,name="viewbookcomic"),
    path('viewbookfatacy_view',views.viewbookfatacy_view,name="viewbookfantacy"),
    path('viewbookmanipulate_view',views.viewbookmanipulate_view,name="viewbookmanipulation"),
    path('booklistview',views.booklistview,name="allcategory"),
    path('logout/', views.logout_view, name='log out'),
    path('booktranaction/',views.booktranaction,name="booktrans"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
