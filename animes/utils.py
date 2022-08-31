from .models import Anime, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def paginateAnimes(request, animes, results):
    page = request.GET.get('page')

    paginator = Paginator(animes, results)

    try:
        animes = paginator.page(page)
    except PageNotAnInteger:
        page=1
        animes = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        animes = paginator.page(page)
    
    leftIndex = 1
    rightIndex = 6
    if int(page) == 1 or int(page) == 2:
        leftIndex = 1
        rightIndex = 6
        if (rightIndex-1) > paginator.num_pages:
            rightIndex = paginator.num_pages + 1
    elif int(page) == paginator.num_pages or int(page) == paginator.num_pages - 1:
        leftIndex = paginator.num_pages - 4
        rightIndex = paginator.num_pages + 1
    else:
        leftIndex = (int(page) - 2)
        rightIndex = (int(page) + 3)

    custom_range = range(leftIndex, rightIndex)
    return custom_range, animes


def searchAnimes(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__iexact=search_query)

    animes = Anime.objects.distinct().filter(
       Q(title__icontains=search_query) |
       Q(tags__in=tags)
    )

    return animes, search_query