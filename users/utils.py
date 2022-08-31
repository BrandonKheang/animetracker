from .models import Profile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print('SEARCH:', search_query)

    profiles = Profile.objects.filter(name__icontains=search_query)
    return profiles, search_query


def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')

    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page=1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    
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
    return custom_range, profiles
