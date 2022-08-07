from rest_framework import generics, permissions, serializers
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin


from .models import Property, PropertyViews 

# Create your tests here.

class PropertySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Property 
        fields = [
            'id',
            'user',
            'title',
            'description',
            'price',
            'tax',
            'country',
            'property_type',
            'advert_type',
            'cover_photo',
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'published_status',
            'views',
            'created_at',
            'updated_at',
        ]
    def get_user(self,obj):
        return obj.user.username

class PropertyCreateSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True) 

    class Meta:
        model = Property 

        exclude = [ "updated_at" , "pkid"]

class PropertyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyViews 
        fields = [
            'pkid',
            'updated_at',
        ]