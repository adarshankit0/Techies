from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from .models import Room, Topic, Message, User, Post, FriendRequest, Contact
from .forms import RoomForm, UserForm, MyUserCreationForm



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email:
            email = email.lower()
        else:
            messages.error(request, "Email is required")
            return render(request, 'base/login_register.html', {'page': 'login'})

        try:
            User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            return render(request, 'base/login_register.html', {'page': 'login'})

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'base/login_register.html', {'page': 'login'})


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')

            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, form.errors)

    return render(request, 'base/login_register.html', {
        'form': form,
        'page': 'register'
    })



def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all().order_by('name')  # 🔥 sorted
    room_messages = Message.objects.all().order_by('-created')[:5]

    return render(request, 'base/home.html', {
        'rooms': rooms,
        'topics': topics,
        'room_messages': room_messages
    })



@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    messages_room = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        if request.user in participants:
            body = request.POST.get("body")
            if body:
                Message.objects.create(
                    user=request.user,
                    room=room,
                    body=body
                )
        else:
            messages.error(request, "Join room first")

        return redirect('room', pk=room.id)

    return render(request, 'base/room.html', {
        'room': room,
        'roomMessages': messages_room,
        'participants': participants
    })



@login_required(login_url='login')
def joinRoom(request, pk):
    room = Room.objects.get(id=pk)
    room.participants.add(request.user)
    return redirect('room', pk=pk)



@login_required(login_url='login')
def createRoom(request):
    topics = Topic.objects.all().order_by('name')  # 🔥 sorted topics

    if request.method == 'POST':

        selected_topic = request.POST.get("topic")

        
        if selected_topic == "new":
            new_topic = request.POST.get("new_topic")

            if new_topic:
                topic_name = new_topic.strip().capitalize()

                
                topic, _ = Topic.objects.get_or_create(name=topic_name)
            else:
                messages.error(request, "Please enter new topic")
                return redirect('create-room')

        else:
            topic = Topic.objects.get(name=selected_topic)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )

        return redirect('home')

    return render(request, 'base/room_form.html', {'topics': topics})


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("Not allowed")

    if request.method == 'POST':
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    return render(request, 'base/room_form.html', {'room': room})


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("Not allowed")

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("Not allowed")

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})



def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()

    request_sent = False

    if request.user.is_authenticated and request.user != user:
        request_sent = FriendRequest.objects.filter(
            sender=request.user,
            receiver=user
        ).exists()

    return render(request, 'base/profile.html', {
        'user': user,
        'rooms': rooms,
        'topics': topics,
        'request_sent': request_sent
    })



@login_required(login_url='login')
def updateUser(request):
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=request.user.id)

    return render(request, 'base/update-user.html', {'form': form})



@login_required(login_url='login')
def sendFriendRequest(request, user_id):
    receiver = User.objects.get(id=user_id)

    if request.user != receiver:
        FriendRequest.objects.get_or_create(
            sender=request.user,
            receiver=receiver
        )

    return redirect('user-profile', pk=user_id)


@login_required(login_url='login')
def acceptFriendRequest(request, request_id):
    req = FriendRequest.objects.get(id=request_id)

    if req.receiver == request.user:
        req.accepted = True
        req.save()

        req.sender.friends.add(req.receiver)
        req.receiver.friends.add(req.sender)

    return redirect('friends')


@login_required(login_url='login')
def friendsPage(request):
    requests = FriendRequest.objects.filter(
        receiver=request.user,
        accepted=False
    )

    friends = request.user.friends.all()

    return render(request, 'base/friends.html', {
        'requests': requests,
        'friends': friends
    })



@login_required(login_url='login')
def postsPage(request):
    posts = Post.objects.all().order_by('-created')

    if request.method == 'POST':
        Post.objects.create(
            user=request.user,
            content=request.POST.get('content'),
            image=request.FILES.get('image')
        )
        return redirect('posts')

    return render(request, 'base/posts.html', {'posts': posts})



def aiPage(request):
    return render(request, 'base/ai.html')


def topicPage(request):
    topics = Topic.objects.all().order_by('name')
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})


def aboutPage(request):
    return render(request, 'base/about.html')


def contactPage(request):
    if request.method == 'POST':
        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )
        return redirect('home')

    return render(request, 'base/contact.html')


def helpPage(request):
    return render(request, 'base/help.html')



@login_required(login_url='login')
def notificationPage(request):
    requests = FriendRequest.objects.filter(
        receiver=request.user,
        accepted=False
    )

    return render(request, 'base/notifications.html', {
        'requests': requests
    })