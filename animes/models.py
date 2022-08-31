from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from users.models import Profile
from django.core.validators import MinValueValidator

# Create your models here.
class Anime(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    anime_length = models.IntegerField(default=9999, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        votes = self.review_set.filter(reviewType='vote')
        upVotes = votes.filter(value='up').count()
        totalVotes = votes.count()
        ratio = round((upVotes / totalVotes)*100)
        
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

    @property
    def noVotes(self):
        self.vote_total = 0
        self.vote_ratio = 0
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    REVIEW_TYPE = (
        ('review', 'Review'),
        ('vote', 'Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    reviewType = models.CharField(max_length=100, choices=REVIEW_TYPE, null=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
