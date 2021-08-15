from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from codingpractice.models import Question, Answer, Coders
from codingpractice.forms import AnswerForm
from django.views.generic.edit import CreateView
from django.views.generic import ListView,DetailView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from django.contrib import messages

# Create your views here.
#@login_required
def index(request):
    #q = Question.objects.all()
    return render(request,'index.html')

def signup(request):
    messages.used=True
    if request.method == 'POST':
        first_name = request.POST['first_name']
        username=first_name
        email= request.POST['email']
        password1= request.POST['password1']
        password2= request.POST['password2']
        
        #form = UserCreationForm(request.POST)
        if password1==password2:
            if User.objects.filter(username=username).exists(): #Checks if username is present or not... No duplicates Allowed
                print("Usertaken")
                messages.info(request,"Username taken")
                messages.used=True      #So that message will b=not repeat again in next query submission
                return render(request,'registration/signup.html')
            elif User.objects.filter(email=email).exists():     #Checks if email is present or not... No duplicates Allowed
                print("Email taken")
                messages.info(request,"Email taken")
                messages.used=True
                return render(request,'registration/signup.html')
            else:
                user= User.objects.create_user(username=first_name,email=email,password=password1)
                user.save()                     #User is created in database this user is normal user not super user
                print('User created')
                return render(request,'registration/login.html')
        else:
            messages.info(request,"Password Doesn't match")
            messages.used=True
            return render(request, 'registration/signup.html')
    else:                                                 #when we just request the page that is get method request
        #messages.info(request,"Error! please fill it again")
        #messages.used=True
        return render(request, 'registration/signup.html')



def login(request):
    if request.method == 'POST':    #When we submit
        
        
        username = request.POST['first_name']
        password = request.POST['password1']
        user = auth.authenticate(username=username, password=password) #Authentication
        
        if user is not None:    #if user is their in database
            auth.login(request,user)

            return redirect('codingpractice:pyques')
        else:
            messages.info(request,"If not have account make here one")
            
            return render(request, 'registration/signup.html')
    else:                                              #when we just request the page that is get method request
        return render(request,'registration/login.html')

@login_required
def pyques(request):
    
    #q=get_object_or_404(Question)
    q=Question.objects.all()
    return render(request,'pyques.html',{'q':q})

@login_required
def solve(request,pk):
    q = Question.objects.get(pk=pk)   # so that question will see on the solve page only the question we have clicked 

    #pk is key to check index from database and used it in urls to show proper specific thing we need

    answer=Answer.objects.get(pk=pk)

    
    if request.method=='POST':  #When we submit

        answer1 = request.POST['answer1']
        with open('coderun.txt','w') as f:
            f.write(answer1)  #because answer name ka textfeild he so answer.answer 
        # Converting above source code to an executable 
        f=open('coderun.txt','r')   #f.readlines will give list 
        a="\n".join(str(i) for i in f.readlines())  #string with \n as middle 
        #print(a)
        
        #execCode = compile(open('coderun.txt','r'), 'mulstring', 'exec') 


        #execCode = compile(a, 'mulstring', 'exec')

        print("\n")
        exec(answer1)           #for debugging
        print("\n")
        ''''w=open('answer_value.txt','w')
        w.write(exec(execCode))

        w1=f.open('answer_value.txt','r')
        print(w1)
        print(type(w1))'''

        #print("\n")
        # Running the executable code. 
        #answer_value = str(exec(execCode))
        #print(answer_value)
        #print("\n")
        #a=get_object_or_404(Answer)
        f.close()
        os.remove('coderun.txt')

        #print(answer.solution)
        print(type(answer.solution))
        print(type(exec(answer1)))
        #print(type(answer_value))
        #print(type(exec(execCode)))
        '''value=""
        for i in answer_value:
            print(i)

            if i != None:
                print(i)
                value=value+i

        print(value)'''

        '''def generator(n): #
            def f(x):
                return x+n
            return f
        plus_one=generator('')
        answer_value=plus_one(answer1)
        print(answer_value)'''

        messages.info(request,"Output")
        messages.info(request,exec(answer1))
        #print(answer_value == answer.solution)
        if answer.solution == "Hello World!":
            messages.info(request,"Success")
            q=Question.objects.all()
            #Coders.UserScore = Coders.UserScore + q.Score
            return render(request,'pyques.html',{'q':q})
        else:
            messages.info(request,"Fail Try again")
            return render(request,'solve.html',{'q':q,'answer':answer1})
    else:
        return render(request,'solve.html',{'q':q,'answer':answer})


@login_required
def logout_view(request):
    logout(request)
    return redirect('codingpractice:index')
