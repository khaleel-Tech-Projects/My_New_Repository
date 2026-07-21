from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from app.models import Detail
from app.models import game


def index(request):
    d1=game.objects.all()
    dict1={
        'data1':d1
    }
    return render(request,'index.html',dict1)
    

def browse(request):
	return render(request,'browse.html')

def details(request):
	return render(request,'details.html')

def streams(request):
	return render(request,'streams.html')

def profile(request):
	return render(request,'profile.html')

def adminmain(request):
    return render(request,'admin.html')

def user(request):
    return render(request,'user.html')

def trending(request):
    return render(request,'trending.html')

def addgame(request):
    if request.method == 'POST':
        link=request.POST['link']
        gamename=request.POST['gamename']
        description=request.POST['description']
        rating=request.POST['rating']
        link1=request.POST['link1']
        d1=game(link=link,gamename=gamename,description=description,rating=rating,link1=link1)
        d1.save()
        return HttpResponseRedirect('/gamelist')
    return render(request,'addgame.html')

def sign(request):
    if request.method == 'POST':
        name=request.POST['name']
        mail=request.POST['mail']
        passw=request.POST['passw']
        rpass=request.POST['rpass']
        d1=Detail(name=name,mail=mail,passw=passw,rpass=rpass)
        if passw == rpass:
            d1.save()
        else:
            return HttpResponseRedirect('/registration')
        
        return HttpResponseRedirect('/login')
    return render(request,'registration.html')

def login(request):
    if request.method == 'POST':
        em=request.POST['mail']
        ps=request.POST['pass']
        data=Detail.objects.all()
        s1=Detail.objects.filter(mail=em,passw=ps).exists()
        if s1 == True:
            if em=='admin@gmail.com':
                return HttpResponseRedirect('/adminmain')
            else:
                return HttpResponseRedirect('/user')
        return HttpResponseRedirect('/user')
    return render(request,'login.html')


def list(request):
  
    d2=Detail.objects.all()
    dict1={
        'data':d2
    }
    return render(request,'userlist.html',dict1)

def delete(request):
    mail=request.GET['mail']
    d1=Detail.objects.get(mail=mail)
    d1.delete()
    return HttpResponseRedirect('/userlist')


def gamelist(request):
    d1=game.objects.all()
    dict1={
        'data1':d1
    }
    return render(request,'gamelist.html',dict1)

