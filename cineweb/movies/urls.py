from django.urls import path,include

from . import views

urlpatterns = [

    path('movies/',views.MovieListCreateView.as_view()),

    path('movies/<str:uuid>/',views.MovieRetreiveUpdateDestroyView.as_view()),

    path('industry/',views.IndustryListCreateView.as_view()),

    path('recommended-movies/<str:uuid>/',views.RecommendedMoviesView.as_view()),

]