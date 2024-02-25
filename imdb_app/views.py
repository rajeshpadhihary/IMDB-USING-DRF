from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import ReviewSerializer,PlatformForStreamingSerializer,MovieSerializer,SearchMovieSerializer
from .models import Movie,PlatformForStreaming,Review

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request):
    data = request.data
    u_token = request.user.auth_token
    if not Token.objects.filter(key=u_token).exists():
        return Response({"error":"Unauthorized User"},status=401)
    try: 
        if Review.objects.filter(review_user=request.user.id, movie=data["movie"]).exists():
            return Response({'error':'You have already submitted a review for this movie.'}, status=200)
            
        else:
            r_user = Users.objects.get(pk=request.user.id)
            m_obj = Movie.objects.get(pk=data['movie'])
            review_save = Review.objects.create(review_user=r_user,rating = data["rating"],movie=m_obj,review_text = data["review_text"])
            review_save.save()
            rating = Review.objects.filter(movie = data["movie"])
            ratings = []
            for i in rating:
                ratings.append(i.rating)
            print(ratings)
            avarage_rating = sum(ratings)/len(ratings)
            m_obj.avg_rating = round(avarage_rating,1) 
            m_obj.number_rating += 1
            m_obj.save()
            return Response("Review added Successfully", status=201)
    except Exception as e:
        return Response(str(e), status=500)

    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reviews(request, movie_id):

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
@permission_classes([IsAuthenticated])
def get_movies(request):
    movies = Movie.objects.all().order_by('title')
    serializer = MovieSerializer(movies,many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_detail(request,pk):
    try:
        movie = Movie.objects.get(id=pk)
        serializer = MovieSerializer(movie)
        data = {}
        if movie.avg_rating  is None or movie.number_rating == 0 :
            data = {"Rating":"N/A","Total Rating": "N/A","Details":serializer.data}
        elif 4 <= movie.avg_rating <= 5:
            data = {"Status":"Best Movie of the season You must have to watch.","Details":serializer.data}
        elif 3 <= movie.avg_rating < 4:
            data = {"Status":"Average Movie Add to your watch list.","Details":serializer.data}
        elif movie.avg_rating < 3:
            data = {"Status":"Worst Movie You may watch or skip this.","Details":serializer.data}
     
        return Response(data)
    except Movie.DoesNotExist:
        return Response("Sorry! The movie does not exist.")

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
@permission_classes([IsAuthenticated])
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