
from django.shortcuts import render
from rhythm.models import Song,Watchlater,History,Channel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Case, When, IntegerField, Value
from django.shortcuts import render, get_object_or_404
def search(request):
    query = request.GET.get("query","")
    

    if query:
       qs = Song.objects.filter(name__icontains= query)
    else:
        qs = Song.objects.all()   

    return render(request, 'rhythm/search.htm',{"songs":qs,"query":query})


def index(request):
    song = Song.objects.all()
    if request.user.is_authenticated:
        user_channel = Channel.objects.filter(name=request.user.username).first()
        if user_channel:
            user_playlist_ids = str(user_channel.music).split(" ")[1:]
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(user_playlist_ids)])
            user_playlist = Song.objects.filter(song_id__in=user_playlist_ids).order_by(preserved)
        else:
            user_playlist = []
    else:
        user_playlist = []
    return render(request,'index.htm',{'song':song,'user_playlist':user_playlist})

def history(request):
    if request.method == "POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user, music_id=music_id)
        history.save()

        return redirect(f"/rhythm/songs/{music_id}")

    history = History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, 'rhythm/history.htm', {"history": song})


def watchlater(request):
    
    if request.method == "POST":
        user = request.user
        video_id = request.POST['video_id']

        watch = Watchlater.objects.filter(user=user)
        
        for i in watch:
            if video_id == i.video_id:
                message = "Your Video is Already Added"
                break
        else:
            watchlater = Watchlater(user=user, video_id=video_id)
            watchlater.save()
            message = "Your Video is Succesfully Added"

        song = Song.objects.filter(song_id=video_id).first()
        return render(request, f"rhythm/songpost.htm", {'song': song, "message": message})

    wl = Watchlater.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, "rhythm/watchlater.htm", {'song': song})


def songs(request):
    song = Song.objects.all()
    return render(request,'rhythm/songs.htm',{'song':song})

def songpost(request,id):
    song = Song.objects.filter(song_id = id).first()
    return render(request,'rhythm/songpost.htm',{'song':song})
def login(request):
   if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        from django.contrib.auth import login
        login(request, user)   
        return redirect("/")
   return render(request, 'rhythm/login.htm')

def signup(request):
         
    if request.method == "POST":
            email = request.POST['email']
            username = request.POST['username']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            if pass1 != pass2:
              messages.error(request, 'Passwords do not match')
              return render(request, 'rhythm/signup.htm')

            if User.objects.filter(username=username).exists():
              messages.error(request, 'Username already exists')
              return render(request, 'rhythm/signup.htm')
           
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = first_name
            myuser.last_name = last_name
            myuser.save()
            user = authenticate(username=username, password=pass1)
            from django.contrib.auth import login
            login(request, user)

            channel = Channel(name=username)
            channel.save()

            return redirect('/')
   # return render(request, 'rhythm/signup.htm',{'song':Song})
    return render(request, 'rhythm/signup.htm')

def logout_user(request):
    auth_logout(request)
    return redirect('login')
    


def channel(request, channel):
    chan = get_object_or_404(Channel, name=channel)
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]
    if not video_ids:
        return render(request, "error.html", {"message": "No valid video IDs found"})

    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    song = Song.objects.filter(song_id__in=video_ids).order_by(preserved)    

    return render(request, "rhythm/channel.htm", {"channel": chan, "song": song})


def upload(request):
    if request.method == "POST":
        name = request.POST['name']
        singer = request.POST['singer']
        tag = request.POST['tag']
        image = request.POST['image']
        movie = request.POST['movie']
       # credit = request.POST['credit']
        song1 = request.FILES['file']

        song_model = Song(name=name, singer=singer, tags=tag, image=image, movie=movie, song=song1)
        song_model.save()

        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name=str(request.user))
        print(channel_find)

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()

    return render(request, "rhythm/upload.htm")



       

    