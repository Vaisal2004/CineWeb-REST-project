from .models import Movie

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import TfidfVectorizer

from django.utils import timezone


def get_recommended_movies(movie):

    data = pd.DataFrame(Movie.objects.filter(active_status=True).values('id','name','industry__name','director__name','tags','genre__name'))



    data['all_fields'] = data['industry__name']+' '+data['director__name']+' '+data['tags']+' '+data['genre__name']
    
    data.drop(columns=['industry__name','director__name','tags','genre__name'],inplace=True)


    tfidf_vectorizer = TfidfVectorizer(max_features=200, stop_words='english')

    vector = tfidf_vectorizer.fit_transform(data['all_fields']).toarray()

    name = movie.name
    
    similiarity=cosine_similarity(vector)

    my_movie_id=data[data['name']==name].index[0]

    distance=sorted(list(enumerate(similiarity[my_movie_id])),reverse=True,key=lambda vector:vector[1])

    recommended_movies_ids=[]

    for i in distance[0:10]:

        similarity_score = i[1]

        ids = data.iloc[i[0]].id

        if similarity_score > 0.1 and ids!=movie.id:

            recommended_movies_ids.append(ids)

    recommended_movies = Movie.objects.filter(id__in=recommended_movies_ids)

    return recommended_movies