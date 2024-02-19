from .models import *
from rest_framework.response import Response
import json
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import ReviewSerializer,PlatformForStreamingSerializer,MovieSerializer,SearchMovieSerializer
from .models import Movie,PlatformForStreaming,Review

# from django.contrib.auth import login, logout

@api_view(['POST'])
@permission_classes([AllowAny])
def add_review(request):
    data = request.data
    try:
        serializer = ReviewSerializer(data=request.data)
        # print(type(serializer),type(data))
        if serializer.is_valid():
            serializer.save()
            rating = Review.objects.filter(movie = data['movie'])
            ratings = []
            for i in rating:
                ratings.append(i.rating)
            # print(ratings)
            avarage_rating = sum(ratings)/len(ratings)
            # print(avarage_rating)
            movie = Movie.objects.get(id=data["movie"])
            # print(movie)
            movie.avg_rating = round(avarage_rating,1) 
            movie.number_rating +=1
            movie.save()
            # return Response(
            #     {
            #         "message": f"Hii {review.review_user}, Your review has been added.", 
            #     }
            # )
            response = {
                        'status': 'success',
                        'message':f"Hii user having user_id {serializer.data['review_user']} ,Your review has been added.",
            }
            return Response(response)
        return Response(serializer.errors)
    except Exception as e:
        return Response({"400": f"{str(e)}"})
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_reviews(request, movie_id):
    data = {}
    try:
        reviews = Review.objects.filter(movie=movie_id)
        serialized_reviews = ReviewSerializer(reviews, many=True).data        
        return Response(serialized_reviews)
    except Exception as e:
        print("Exception in getting reviews : ", str(e))
        return Response({'error':'Something went wrong while fetching the reviews'})
    

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_review(request, id):
    try:
        review = Review.objects.get(id=id)
        movie_name = review.movie
        movie = Movie.objects.get(title=movie_name)
        movie_id = movie.id
        review.delete()
        rating = Review.objects.filter(movie = movie_id)
        ratings = []
        for i in rating:
            ratings.append(i.rating)
        print(ratings)
        avarage_rating = sum(ratings)/len(ratings)
        movie.avg_rating = round(avarage_rating,1) 
        movie.number_rating -= 1
        movie.save()

        return Response({"message":"Review deleted successfully"},status=200)
    except Review.DoesNotExist:
        return Response({"error":"This review does not exist."},status=404)
    except Exception as e:
        return Response({"error":f"An error occurred while deleting the review - {str(e)}"},status=500)
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_movie(request):
    try:
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors)
    except Exception as e:
        return Response({"400": f"{str(e)}"})
    
@api_view(['GET'])
@permission_classes([AllowAny])
def get_movies(request):
    movies = Movie.objects.all().order_by('title')
    serializer = MovieSerializer(movies,many=True)
    
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([AllowAny])
def search_movies(request):
    try:
        movie_name = request.data['search']
        queryset = Movie.objects.filter(title__icontains = movie_name)
        
        if len(queryset) == 0:
            return Response({'error':f"No movies found containing {movie_name}"})
        else:
            serializer = SearchMovieSerializer(queryset, many=True)
            return Response(serializer.data)
            
    except KeyError:
        return Response({'error':"Please provide a search term"})
        
    except Exception as e:
        return Response({'error':str(e)})

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_movie(request, id):
    try:
        movie = Movie.objects.get(id=id)
        movie_name = movie.title
        movie_id = Movie.objects.get(title = movie_name)
        review = Review.objects.filter(movie = movie_id.id)
        review.delete()
        movie.delete()

        return Response({"message":"Movie deleted successfully"},status=200)
    except Review.DoesNotExist:
        return Response({"error":"This Movie does not exist."},status=404)
    except Exception as e:
        return Response({"error":f"An error occurred while deleting the Movie - {str(e)}"},status=500)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_stream_platform(request):
    try:
        serializer = PlatformForStreamingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    except Exception as e:
        return Response({"400": f"{str(e)}"})
    
@api_view(['GET'])
@permission_classes([AllowAny])
def stream_platform_list(request):
    platforms = PlatformForStreaming.objects.all()
    serializer = PlatformForStreamingSerializer(platforms, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_stream_platform(request, id):
    try:
        platform = PlatformForStreaming.objects.get(id=id)
        platform_id = platform.id
        platform_movies = Movie.objects.filter(stream_platform = platform_id)
        platform_movies.delete()
        platform.delete()
        return Response({"message":"platform deleted successfully"},status=200)
    except Review.DoesNotExist:
        return Response({"error":"This platform does not exist."},status=404)
    except Exception as e:
        return Response({"error":f"An error occurred while deleting the platform - {str(e)}"},status=500)