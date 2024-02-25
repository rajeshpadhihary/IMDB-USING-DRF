from rest_framework import serializers
from .models import PlatformForStreaming,Movie,Review

class PlatformForStreamingSerializer(serializers.ModelSerializer):
    # movie = MovieSerializer(many = True,read_only = True)
    class Meta:
        model = PlatformForStreaming
        # exclude = ('movieList',)
        fields = [
            "id",
            "name",
            "about",
            'website',
        ]

    def create(self, validated_data):
        name = validated_data["name"]
        about = validated_data["about"]
        website = validated_data["website"]
      
        if PlatformForStreaming.objects.filter(name=name).exists() or PlatformForStreaming.objects.filter(website = website).exists():
            raise serializers.ValidationError({'error': 'This platform/website is already exists.'})        
        else:
            stream_platform = PlatformForStreaming.objects.create(name=name, about=about, website=website)
            stream_platform.save()
        return stream_platform

class MovieSerializer(serializers.ModelSerializer):
    stream_platform = PlatformForStreamingSerializer()
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "movie_summary",
            'stream_platform',
        ]
    

    def create(self, validated_data):
        movie_name = validated_data["title"]
        movie_summary = validated_data["movie_summary"]
        stream_platform = validated_data["stream_platform"]

        if PlatformForStreaming.objects.filter(name = stream_platform).exists():
            movie =  Movie.objects.create(title = movie_name , movie_summary = movie_summary, stream_platform = stream_platform)
            movie.save()
            return movie
        
        else:
            raise serializers.ValidationError({'error':'The provided streaming platform does not exist!'})
       

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            "id",
            "review_user",
            "rating",
            "movie",
            "review_text",
        ]
    
    
class SearchMovieSerializer(serializers.ModelSerializer):
    stream_platform = PlatformForStreamingSerializer()
    class Meta:
        model = Movie
        fields = ['title','avg_rating','stream_platform','movie_summary']
    