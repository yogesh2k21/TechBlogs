from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from BlogFeed.models import Post
from django.contrib.auth import login, logout , authenticate
from django.contrib.auth.models import User
from django.db.models import Max


# Create your views here.
def home(request):
    allposts=Post.objects.all()
    context={'content':allposts}
    return render(request,'home/home.html',context)

def about(request):
    return render(request,'home/about.html')

def contact(request):
    if request.method=='POST':
        name=request.POST.get("name",'')
        mail=request.POST.get("email",'')
        phone=request.POST.get("phone",'')
        issue=request.POST.get("issue",'')
        if len(name)<2 or len(mail)<3 or len(phone)<10 or len(issue)<5:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name,email=mail,phone=phone,issue=issue)
            contact.save()
            messages.success(request, "Your form has been successfully sent")
    return render(request,'home/contact.html')

def search(request):
    query=request.GET['query']
    if len(query)>50:
        data=Post.objects.none()
        params={'allposts':data,'query':query}
    else:
        datatitle=Post.objects.filter(title__icontains=query)
        datacontent=Post.objects.filter(content__icontains=query)
        dataauthor=Post.objects.filter(author__icontains=query)
        data=datatitle.union(dataauthor,datacontent)
        params={'allposts':data,'query':query}
    if data.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    return render(request,'home/search.html',params)

#APIs
def handlesignup(request):
    if request.method=="POST":
        username=request.POST['username']
        fn=request.POST['first']
        ln=request.POST['last']
        email=request.POST['email']
        password1=request.POST['pass']
        password2=request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request,"Account already exists!!")
            return render(request,'home/contact.html')
        #logic for same username    
        if User.objects.filter(email=email):
            messages.error(request,"Account already exists!!")
            return render(request,'home/contact.html')
        #logic for same password
        if password1!=password2:
            messages.error(request,"Please Enter Same Passwords!!")
            return render(request,'home/contact.html')
        #logic for alfanumeric username
        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers!!")
            return render(request,'home/contact.html')
        #creating user
        myuser=User.objects.create_user(username,email,password1)
        print(myuser)
        myuser.first_name=fn
        myuser.last_name=ln
        myuser.save()
        messages.success(request, "Your Account has been successfully created")
        return redirect('/')

    return HttpResponse("Not Found")

def handlelogin(request):
    if request.method=="POST":
        loginusername=request.POST['username']
        loginpassword=request.POST['password']
        user=authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials!")
            return redirect('contact')

    return HttpResponse("Login")

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')

