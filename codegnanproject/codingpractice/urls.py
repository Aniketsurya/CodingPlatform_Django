from django.urls import path
from codingpractice.views import index,signup,logout_view,login,pyques,solve

app_name = 'codingpractice'

urlpatterns = [
    path('',index,name = 'index'),
    path('signup/',signup,name = 'signup'),
    path('login/',login,name = 'login'),
    path('pyques/',pyques,name = 'pyques'), #List of questions page
    path('solve/<int:pk>/',solve,name = 'solve'),   #Solving page

    path('logout/',logout_view,name = 'logout'),
    ]

