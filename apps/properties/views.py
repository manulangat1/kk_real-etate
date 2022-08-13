from cgitb import lookup
from django.shortcuts import render
import logging 
import django_filters 
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters, generics, permissions, status 
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response 
from rest_framework.views import APIView 
from .exceptions import PropertyNotFound 
from .models import Property , PropertyViews 
from .pagination import PropertyPagination 
from .serializers import (
    PropertyCreateSerializer,
    PropertyViewSerializer,
    PropertySerializer
)

# Create your views here.


logger = logging.getLogger(__name__)


class PropertyFilter(django_filters.FilterSet):
    advert_type = django_filters.ChoiceFilter(
        field_name="advert_type", lookup_expr="iexact"
    )
    proprty_type = django_filters.CharFilter(
        field_name="property_type" , lookup_expr="iexact"
    )
    price = django_filters.NumberFilter(
        
    )
    price__gt = django_filters.NumberFilter(
        field_name="price", lookup_expr="gt"
    )
    price__lt = django_filters.NumberFilter(
        field_name="price", lookup_expr="lt"
    )

    class Meta:
        model = Property 
        fields = [ 
            "advert_type",
            "property_type",
            "price"
        ]


class ListAllPropertiesAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer 
    queryset = Property.objects.all().order_by("-created_at")
    pagination_class = PropertyPagination 
    filter_backends = [ 
        DjangoFilterBackend , 
        filters.SearchFilter  , 
        filters.OrderingFilter
    ]
    filterset_class = PropertyFilter 
    search_fields = [ 
        "country",
        "city"
    ]
    ordering_fields = [ 
        "created_at"
    ]

class ListAgentsPropertyAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination 
    filter_backends = [ 
        DjangoFilterBackend , 
        filters.SearchFilter  , 
        filters.OrderingFilter
    ]
    filterset_class = PropertyFilter 
    search_fields = [ 
        "country",
        "city"
    ]
    ordering_fields = [ 
        "created_at"
    ]

    def get_queryset(self):
        user = self.request.user 
        queryset = Property.objects.filter(user=user).order_by('-created_at')
        return queryset 


class PropertyViewsAPIView(generics.ListAPIView):
    serializer_class = PropertyViewSerializer
    queryset = PropertyViews.objects.all()

class PropertyDetailView(APIView):
    def get(self,request,slug):
        property = Property.objects.get(slug=slug) 
        x_forwarded_for = request.META.get("HTTP_X_FORWADED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        if not PropertyViews.objects.filter(property=property, ip =ip).exists():
            PropertyViews.objects.create(property=property, ip=ip)
            property.views += 1 
            property.save()
        serializer = PropertySerializer(property , context = {
            'request':request
        })
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_property_api_view(request,slug):
    try:
        property = Property.objects.get(slug=slug)
    except property.DoesNotExist():
        raise PropertyNotFound
    user = request.user 
    if property.user != user:
        return Response(
            {"error": "You do not have permissions to do this"},
            status=status.HTTP_403_FORBIDDEN
        )

