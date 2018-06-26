from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import pyrebase
from django.contrib import auth

config={

'apiKey': "AIzaSyBFjx2x7okiqSL6s6OPsdlVYyfzbpTzbnE",
    'authDomain': "cpanel-a08d4.firebaseapp.com",
    'databaseURL': "https://cpanel-a08d4.firebaseio.com",
    'projectId': "cpanel-a08d4",
    'storageBucket': "cpanel-a08d4.appspot.com",
    'messagingSenderId': "991888837993"
  };
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()

def signin(request):
    return render(request,"login.html")



from sentimenter.sentimenter import primary
from .forms import userinput

from sentimenter import *

# Create your views here.
def index(request):
    user_input=userinput()
    return render(request,"index.html",{'hashtag':user_input})

def login(request):
    user_input=userinput()
    return render(request,"login.html",{'hashtag':user_input})

def analyze(request):
    user_input=userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        hashtag=user_input.cleaned_data['q']
        print(hashtag)
        data=primary(hashtag)
        return render(request,"result.html",{'data':data})
    return render(request,"index.html",{'hashtag':user_input})

def postsignin(request):
    email=request.POST.get('username')
    password=request.POST.get('password')
    try:
        user=authe.sign_in_with_email_and_password(email,password)
        user_input = userinput(request.GET or None)
        if request.GET and user_input.is_valid():
            hashtag = user_input.cleaned_data['q']
            print(hashtag)
            data = primary(hashtag)

    except:
        message="Invalid Credentials"
        return render(request,"login.html",{"message":message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "index.html", {'hashtag': user_input, 'email': email})

def logout(request):
    auth.logout(request)
    return render(request,'login.html')

def signup(request):
    return render(request,"signup.html")
def postsignup(request):
    name=request.POST.get('name')
    email=request.POST.get('username')
    password=request.POST.get('password')
    try:
        user=authe.create_user_with_email_and_password(email,password)
    except:
        message="Unable to create account try again"
        return render(request,"login.html",{"message":message})
    uid=user['localId']
    data={"name":name,"status":"1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request,"login.html")

def contact(request):
    return render(request,"contact.html")

def postfeedback(request):
    import time
    from datetime import datetime,timezone
    import pytz

    tz=pytz.timezone('Asia/Kolkata')
    time_now=datetime.now(timezone.utc).astimezone(tz)
    milis=int(time.mktime(time_now.timetuple()))
    email = request.POST.get('email')
    feedback=request.POST.get('feedback')
    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    a=a['localId']
    data = {
        "work": email,
        "feedback": feedback
    }

    database.child('users').child(a).child('feedback').child(milis).set(data)
    message="Your feedback has been submitted!!!!"
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        hashtag = user_input.cleaned_data['q']
        print(hashtag)
        data = primary(hashtag)
    return render(request, "index.html", {'hashtag': user_input, 'message': message})

def check(request):
    import datetime
    idtoken=request.session['uid']
    a=authe.get_account_info(idtoken)
    a=a['users']
    a=a[0]
    a=a['localId']

    timestamps=database.child('users').child(a).child('feedback').shallow().get().val()
    lis_time=[]
    for i in timestamps:
        lis_time.append(i)
    lis_time.sort(reverse=True)

    work=[]

    for i in lis_time:
        wor=database.child('users').child(a).child('feedback').child(i).child('work').get().val()
        work.append(wor)
    print(wor)
    print(work)

    date=[]
    for i in lis_time:
        i=float(i)
        dat=datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')

    comb_list=zip(lis_time,date,work)

    return render(request,'check.html',{'comb_list':comb_list})







