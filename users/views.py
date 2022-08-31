from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Message
from animes.models import Anime, Review
from .forms import CustomUserCreationForm, ProfileForm, MessageForm
from animes.forms import VoteForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginateProfiles

# Create your views here.

def loginUser(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('animes')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'animes')
        else:
            messages.error(request, 'Username OR password is incorrect')
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account successfully created!')

            login(request, user)
            return redirect('animes')

        else:
            messages.error(request, 'An error has accoured during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 15)
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    animes = profile.animes.all()
    context = {'profile':profile, 'animes':animes}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    animes = profile.animes.all()
    context = {'profile': profile, 'animes': animes}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def deleteAnime(request, pk):
    profile = request.user.profile
    anime = profile.animes.get(id=pk)
    reviews = anime.review_set.all()
    for review in reviews:
        if review.owner == profile:
            review.delete()
    if request.method == 'POST':
        profile.animes.remove(anime)
        return redirect('account')
    context = {'anime': anime}
    return render(request, 'users/delete_template.html', context)


@login_required(login_url='login')
def addAnime(request, pk):
    profile = request.user.profile
    anime = Anime.objects.get(id=pk)
    form = VoteForm()
    if request.method == 'POST':
        profile.animes.add(anime)
        form = VoteForm(request.POST)
        review = form.save(commit=False)
        review.anime = anime
        review.owner = request.user.profile
        review.reviewType = 'vote'
        review.save()
        anime.getVoteCount
        url = 'http://127.0.0.1:8000/anime/{0}'.format(pk)
        messages.success(request, 'Your review was successfully submitted!')
        return redirect(url)
    
    context = {'anime': anime, 'form': form}
    return render(request, 'users/add_template.html', context)
    

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)


def editAnime(request, pk):
    user = request.user.profile
    reviews = Review.objects.all()
    for review in reviews:
        if(review.owner == user):
            currentReview = review
    anime = Anime.objects.get(id=pk)
    form = VoteForm(instance=currentReview)

    if request.method == 'POST':
        form = VoteForm(request.POST, instance=currentReview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your vote was editted')

            return redirect('account')
    context = {'form': form, 'anime':anime}
    return render(request, 'users/add_template.html', context)