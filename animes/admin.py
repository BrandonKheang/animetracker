from django.contrib import admin

# Register your models here.
from .models import Anime, Review, Tag

admin.site.register(Anime)
admin.site.register(Review)
admin.site.register(Tag)