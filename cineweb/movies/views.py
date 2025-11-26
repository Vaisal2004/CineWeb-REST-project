from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from .models import Movie,Industry

from .serializers import MovieSerializer,MovieWriteSerializer,IndustrySerializer

from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import AllowAny

from authentication.permissions import IsAdmin,IsUser

from .recommendations import get_recommended_movies

# Create your views here.

class MovieListCreateView(APIView):

    authentication_classes = [JWTAuthentication]

    serializer_class = MovieSerializer

    serializer_write_class = MovieWriteSerializer

    http_method_names = ['get','post']

    def get_permissions(self):

        if self.request.method == 'GET':

            return[AllowAny()]
        
        elif self.request.method == 'POST':

            return[IsAdmin()]
        
        return super().get_permissions()

    def get(self,request,*args,**kwargs):

        movies = Movie.objects.filter(active_status=True) 

        serializer = self.serializer_class(movies,many=True)

        return Response(serializer.data)
    
    def post(self,request,*args,**kwargs):

        movie_data = request.data

        serializer = self.serializer_write_class(data=movie_data)

        if serializer.is_valid():

            serializer.save()

            data = {'msg':'movie created successfully'}

            return Response(data)
        
        return Response(serializer.errors,status=400)
    
class MovieRetreiveUpdateDestroyView(APIView):

    serializer_class = MovieSerializer

    serializer_write_class = MovieWriteSerializer

    http_method_names = ['get','put','delete']

    def get_permissions(self):

        if self.request.method == 'GET':

            return [AllowAny()]
        
        elif self.request.method in ['PUT',"DELETE"]:

            return [IsAdmin()]
        
        return super().get_permissions()

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        serializer = self.serializer_class(movie)

        return Response(serializer.data)
    
    def put(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        movie_data = request.data

        serializer = self.serializer_write_class(movie,data=movie_data,partial=True)

        if serializer.is_valid():

            serializer.save()

            data = {'msg':'movie updated successfully'}

            return Response(data)
        
        return Response(serializer.errors,status=400)
    
    def delete(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        movie.active_status = False

        movie.save()

        data = {'msg':'movie deleted successfully'}

        return Response(data)
    
class IndustryListCreateView(APIView):

    serializer_class = IndustrySerializer

    def get(self,request,*args,**kwargs):

        industry = Industry.objects.filter(active_status=True)

        serializer = self.serializer_class(industry,many=True)

        return Response(serializer.data)
    
    def post(self,request,*args,**kwargs):

        industry_data = request.data

        serializer = self.serializer_class(data=industry_data)

        if serializer.is_valid():

            serializer.save()

            data = {'msg':'industry created successfully'}

            return Response(data)
        
        return Response(serializer.errors,status=400)
    
class IndustryRetrieveUpdateDestroyView(APIView):

    def get(self,request,*args,**kwargs):

       uuid = kwargs.get('uuid')

       industry = Industry.objects.get(uuid=uuid)

       serializer = self.serializer_class(industry)

       return Response(serializer.data)
     
class RecommendedMoviesView(APIView):

    authentication_classes = [JWTAuthentication]

    serializer_class = MovieSerializer

    http_method_names = ['get']

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        movie = Movie.objects.get(uuid=uuid)

        reccommended_movies = get_recommended_movies(movie)

        serializer = self.serializer_class(reccommended_movies,many=True)

        return Response(serializer.data)