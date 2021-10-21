from django.urls import path
from store import views

urlpatterns=[
    path('',views.home,name= 'home'),
    path('patient',views.patient,name='patient'),
    path('doctor',views.doctor,name='doctor'),
    path('profile',views.profile,name = 'profile'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout'),

    path('bloghome',views.bloghome,name='bloghome'),
    path('mypost',views.mypost,name='mypost'),
    path('newpost',views.newpost,name='newpost'),
    path('postview/<int:id>',views.postview,name='postview'),
    path('updatepost/<int:id>',views.updatepost,name='updatepost'),

]