from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Anime, Tag, Review
from .forms import AnimeForm, ReviewForm
from users.models import Profile
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import searchAnimes, paginateAnimes

# Create your views here.
def animes(request):
    animes, search_query = searchAnimes(request)
    custom_range, animes = paginateAnimes(request, animes, 15)

    for anime in animes:
        if(anime.review_set.filter(reviewType='vote').count() > 0):
            anime.getVoteCount
        else:
            anime.noVotes

    context = {'animes': animes, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, 'anime/animes.html', context)


def anime(request, pk):
    animeObj = Anime.objects.get(id=pk)
    tags = animeObj.tags.all()
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.anime = animeObj
        review.owner = request.user.profile
        review.reviewType = 'review'
        review.save()
        animeObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('anime', pk=animeObj.id)
    context = {'anime': animeObj, 'tags': tags, 'form': form}
    return render(request, 'anime/anime.html', context)


@login_required(login_url="login")
def createAnime(request):
    form = AnimeForm()

    if request.method == 'POST':
        form = AnimeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('animes')

    context = {'form': form}
    return render(request, "anime/anime_form.html", context)


def genres(request, pk):
    genres = Tag.objects.all()
    genre = genres.get(id=pk)

    animes, search_query = searchAnimes(request)
    filteredAnimes = []
    for anime in animes:
        if genre in anime.tags.all():
            filteredAnimes.append(anime)
    custom_range, filteredAnimes = paginateAnimes(request, filteredAnimes, 15)

    context = {'genre': genre, 'animes': filteredAnimes, 'search_query': search_query, 'custom_range':custom_range}
    return render(request, 'anime/genre_template.html', context)


def deleteReview(request, pk):
    review = Review.objects.get(id=pk)
    animeId = review.anime.id
    review.delete()
    messages.info(request, 'Your review was deleted')
    return anime(request, animeId)
    
