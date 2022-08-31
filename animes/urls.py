from django.urls import path
from . import views
from users import views as userViews

urlpatterns = [
    path('', views.animes, name="animes"),
    path('anime/<str:pk>/', views.anime, name="anime"),
    path('create-anime/', views.createAnime, name="create-anime"),
    path('genres/<str:pk>/', views.genres, name="genres"),
    path('delete-review/<str:pk>/', views.deleteReview, name="delete-review"),

    path('users/add-anime/<str:pk>/', userViews.addAnime, name="add-anime"),
]