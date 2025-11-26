from django.db import models

# Create your models here.

import uuid

class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        abstract = True

class Industry(BaseClass):

    name = models.CharField(max_length=25)

    class Meta :

        verbose_name = 'Industry'

        verbose_name_plural = 'Industry'

    def __str__(self):

        return self.name
    
class Genre(BaseClass):

    name = models.CharField(max_length=25)

    class Meta :

        verbose_name = 'Genre'

        verbose_name_plural = 'Genre'

    def __str__(self):

        return self.name
    
class Director(BaseClass):

    name = models.CharField(max_length=25)

    dob = models.DateField()

    no_of_movies = models.IntegerField()

    class Meta :

        verbose_name = 'Director'

        verbose_name_plural = 'Director'

    def __str__(self):

        return self.name

class Movie(BaseClass):

    name = models.CharField(max_length=50)

    banner = models.ImageField(upload_to='movies/images')

    release_date = models.DateField()

    industry = models.ForeignKey('Industry',on_delete=models.CASCADE)

    genre = models.ManyToManyField('Genre')

    director = models.ForeignKey('Director',on_delete=models.CASCADE)

    tags = models.TextField()

    class Meta :

        verbose_name = 'Movies'

        verbose_name_plural = 'Movies'

    def __str__(self):

        return f'{self.name}-{self.industry.name}'
