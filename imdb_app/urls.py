from django.urls import path
from .views import add_review,get_reviews,delete_review,add_movie,get_movies,add_stream_platform,stream_platform_list,delete_movie,search_movies,delete_stream_platform


urlpatterns = [
    path("add_review/",add_review,name='add_review'),
    path("get_review/<int:movie_id>/",get_reviews, name="get_reviews"),
    path("delete_review/<int:id>/",delete_review, name="delete_review"),
    path("add_movie/",add_movie, name="add_movie"),
    path('movie_list/',get_movies, name='movie_list'),
    path("get_specific_movie/",search_movies, name="get_specific_movie"),
    path("delete_movie/<int:id>/",delete_movie, name="delete_movie"),
    path('add_platform/',add_stream_platform, name='add_platform'),
    path('platform_list/',stream_platform_list, name='platform_list'),
    path("delete_stream_platform/<int:id>/",delete_stream_platform, name="delete_stream_platform"),
]