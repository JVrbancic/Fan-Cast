from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages, sessions
from .models import*
from time import gmtime, strftime
from datetime import datetime
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


# Create your views here.

def index(request):
    now = datetime.now()
    
    year = now.strftime("%Y")
    print("year:", year)

    month = now.strftime("%m")
    print("month:", month)

    day = now.strftime("%d")
    print("day:", day)

    time = now.strftime("%H:%M:%S")
    print("time:", time)

    date_time = now.strftime("%b.%d.%Y")
    print("date is:",date_time)	

    context ={
        "date":date_time,
    }
    return render(request, 'index.html', context)

def register(request):
    #validations
    error=False
    if len(request.POST['f_name'])<2:
        error= True
        messages.error(request,'First Name must be gt 3')
    if len(request.POST['l_name'])<2:
        error= True
        messages.error(request,'Last Name must be gt 3')
    if len(request.POST['email'])<2:
        error= True
        messages.error(request,'Email must be gt 3')    
    if len(request.POST['password'])<8:
        error= True
        messages.error(request,'PW must be gt 8')
    if request.POST['password'] != request.POST['c_password']:
        error= True
        messages.error(request,'Password must match', extra_tags='passwords must match')
    #Email regrex
    if not EMAIL_REGEX.match(request.POST['email']):
        error=True
        messages.error(request,"Invalid Email Address!")
        
        
    #name alpha
    if not request.POST['f_name'].isalpha():
        messages.error(request,"first name must not contain numbers or symbols")
        error=True
    if not request.POST['l_name'].isalpha():
        messages.error(request,"last name must not contain numbers or symbols")
        error=True
    if error==True:
        return redirect('/')


    #email already exists

    if User.objects.filter(email=request.POST['email']):
        error=True
        messages.error(request, 'User already exists')
    #if bad, redirect ('/')
    if error:
        messages.error(request,'Please try to re-register.')
        return redirect('/')
   
    #if good, encrypt password
    hashed=bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
    decoded_hash=hashed.decode('utf-8')

    #decode
    user=User.objects.create(f_name=request.POST['f_name'],l_name=request.POST['l_name'],user_name=request.POST['user_name'],email=request.POST['email'],password=decoded_hash)
    #store in db
    
    #store something in session
    request.session['u_id']=user.id
   
    print("user added into session")
    #redirect ('/') or where appropriate
    
    messages.success(request,"you have successfully registered now please log in")
    return redirect('/main')

def login(request):
    #grab user based on email
    user_list=User.objects.filter(email=request.POST['email'])
    if not user_list:
        messages.error(request, 'invalid credentials')
        return redirect('/')
    user=user_list[0]
    if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
        request.session['u_id']=user.id
        print(user.id)
        return redirect('/main')
    else:
        messages.error(request,'pass is bad')
    return redirect('/')
    #if there, continue, else redirect
    #check pw
    #store in session

def logout(request):
    request.session.clear()
    return redirect('/')

def main(request):
    #    if not in session redirect out 
    if not 'u_id' in request.session:
        return redirect('/')

    now = datetime.now()    
    year = now.strftime("%Y")
    print("year:", year)
    month = now.strftime("%m")
    print("month:", month)
    day = now.strftime("%d")
    print("day:", day)
    time = now.strftime("%H:%M:%S")
    print("time:", time)
    date_time = now.strftime("%b.%d.%Y")
    print("date is:",date_time)

    comiclast=Topic.objects.filter(genre="comics").last()
    videogamelast=Topic.objects.filter(genre="video_games").last()
    booklast=Topic.objects.filter(genre="books").last()
    
    context ={
        "date":date_time,
        "user":User.objects.get(id=request.session["u_id"]),
        "comlast":Topic.objects.filter(genre="comics").last(),
        "vglast":Topic.objects.filter(genre="video_games").last(),
        "bolast":Topic.objects.filter(genre="books").last(),
        "topic":Topic.objects.all(),
        "comgen":Topic.objects.filter(genre="comics").exclude(id=comiclast.id),
        "vggen":Topic.objects.filter(genre="video_games").exclude(id=videogamelast.id),
        "bogen":Topic.objects.filter(genre="books").exclude(id=booklast.id),
        # "genre":Topic.objects.
    }

    return render(request, 'main.html', context)

def add(request):
#    if not in session redirect out 
    if not 'u_id' in request.session:
        return redirect('/')
   
    context ={
        "user":User.objects.get(id=request.session["u_id"]),
    }
   

    return render(request, 'add.html', context)
    
    
def adder(request):
    error=False

    #  validations
    if not 'u_id' in request.session:
        messages.error(request, 'Must be logged in as a user to add character topics')
        return redirect('/add')
        print('user not logged into session')
    if len(request.POST['name'])<3:
        error= True
        messages.error(request,'Character Name must be gt 3')
        print('name must be gt 3')
        return redirect('/add')
    if error==False:
        Topic.objects.create(name=request.POST['name'], genre=request.POST['genre'],user=User.objects.get(id=request.session['u_id']), image=request.FILES['image'])
        return redirect('/main')





def adder_post(request):
    error=False

    topic=Topic.objects.get(id=request.POST['topic'])
    topic_id=topic.id
    

    #  validations
    if not 'u_id' in request.session:
        messages.error(request, 'Must be logged in as a user to post to topics')
        return redirect('/post/' + topic_id)
        print('user not logged into session')
    if len(request.POST['actor_name'])<3:
        error= True
        messages.error(request,'Character Name must be gt 3')
        print('name must be gt 3')
        return redirect('/post/' + str(topic_id))
    
    context={
        "topic":Topic.objects.get(id=topic_id),
        "user":User.objects.get(id=request.session["u_id"]),
    }

    if error==False:
        
        Post.objects.create(user=User.objects.get(id=request.session['u_id']), actor_name=request.POST['actor_name'],topic=Topic.objects.get(id=topic.id) , image=request.FILES['headshot'])
        return redirect('/topic/'+ str(topic_id))


def logout(request):
    request.session.clear()
    print('session cleared')
    return redirect('/')

def topic(request,topic_id):
    if not 'u_id' in request.session:
        return redirect('/')
    print(request.session)

    context={
        "topic":Topic.objects.get(id=topic_id),
        "user":User.objects.get(id=request.session["u_id"]),
        "posts":Post.objects.filter(topic=topic_id),
    }
    return render(request, 'topic.html', context)

def post(request,topic_id):
    if not 'u_id' in request.session:
        return redirect('/')
    print(request.session)

    context={
        "topic":Topic.objects.get(id=topic_id),
        "user":User.objects.get(id=request.session["u_id"]),
    }
    return render(request, 'post.html', context)


def myaccount(request,user_id):
    if not 'u_id' in request.session:
        return redirect('/')
    context ={
        "user":User.objects.get(id=request.session["u_id"]),
    }
    return render(request,'myaccount.html', context)

def update(request):
    if not 'u_id' in request.session:
        return redirect('/')
    
    user=User.objects.get(id=request.session['u_id'])


    #trying to edit email to that of which one already exists
    
    error=False
     #email already exists
    if User.objects.filter(email=request.POST['email']).exclude(email=user.email):
        error=True
        messages.error(request,'email already in use')
    # elif User.objects.filter(email=request.POST['email']):
    #     error=True
    #     messages.error(request, ' email was kept the same')
    #email regrex
    if not EMAIL_REGEX.match(request.POST['email']):
        error=True
        messages.error(request,"Invalid Email Address!")

    if User.objects.filter(user_name=request.POST['user_name']).exclude(user_name=user.user_name):
        error=True
        messages.error(request,'That User-Name is already exists')

    if error:
        messages.error(request,'Reverting back to original stored information, no update has been made.')
        return redirect('/myaccount/'+str(user.id))
   
    if error==False:      
        user.f_name=request.POST['f_name']
        user.l_name=request.POST['l_name']
        user.email=request.POST['email']
        user.user_name=request.POST['user_name']
        user.save()
        messages.success(request,"you have successfully edited")
        return redirect('/myaccount/'+str(user.id))
    return redirect('/myaccount/'+str(user.id))

def genre_com(request):
#    if not in session redirect out 
    if not 'u_id' in request.session:
        return redirect('/')
    context ={
        "user":User.objects.get(id=request.session["u_id"]),
        "topic":Topic.objects.all(),
        "comgen":Topic.objects.filter(genre="comics").exclude(name="comgenEx"),
        "vggen":Topic.objects.filter(genre="video_games"),
        "bogen":Topic.objects.filter(genre="books"),
    }

    return render(request, 'genre_com.html', context)

def genre_vg(request):
#    if not in session redirect out 
    if not 'u_id' in request.session:
        return redirect('/')
    context ={
        "user":User.objects.get(id=request.session["u_id"]),
        "topic":Topic.objects.all(),
        "comgen":Topic.objects.filter(genre="comics").exclude(name="comgenEx"),
        "vggen":Topic.objects.filter(genre="video_games"),
        "bogen":Topic.objects.filter(genre="books"),
    }

    return render(request, 'genre_vg.html', context)

def genre_book(request):
#    if not in session redirect out 
    if not 'u_id' in request.session:
        return redirect('/')
    context ={
        "user":User.objects.get(id=request.session["u_id"]),
        "topic":Topic.objects.all(),
        "comgen":Topic.objects.filter(genre="comics").exclude(name="comgenEx"),
        "vggen":Topic.objects.filter(genre="video_games"),
        "bogen":Topic.objects.filter(genre="books"),
    }

    return render(request, 'genre_book.html', context)

def add_like(request):
    #    if not in session redirect out 
    if not 'u_id' in request.session:
        return redirect('/')

    print('like function')

    topic=Topic.objects.get(id=request.POST['topic'])
    topic_id=topic.id

    post = Post.objects.get(id=request.POST['post_id'])
    post.liked_by.add(User.objects.get(id=request.session['u_id']))

    context={
        "topic":Topic.objects.get(id=topic_id),
        "user":User.objects.get(id=request.session["u_id"]),
    }
    
    return redirect('/topic/'+ str(topic_id))


def post_remove(request,topic_id,post_id):
     #    if not in session redirect out 
    if not 'u_id' in request.session:
        return redirect('/')
    

    
    post=Post.objects.get(id=post_id)
    post.delete()

    return redirect('/topic/'+ str(topic_id))



def like_remove(request,topic_id,post_id):
     #    if not in session redirect out 
    if not 'u_id' in request.session:
        return redirect('/')
    

    post = Post.objects.get(id=post_id)
    post.liked_by.remove(User.objects.get(id=request.session['u_id']))    


    return redirect('/topic/'+ str(topic_id))