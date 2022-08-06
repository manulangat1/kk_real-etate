from django.shortcuts import render
from rest_framework import generics , permissions , status 
from rest_framework.response import Response
from rest_framework.views import APIView
from .exceptions import ProfileNotFound , NotYourProfile
from .models import Profile 
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer , UpdateProfileSerializer

# Create your views here.

class AgentListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)
    queryset = Profile.objects.filter(is_agent=True)


class TopAgentsListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)
    queryset = Profile.objects.filter(top_agent=True)


class GetProfileAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    # serializer_class = ProfileSerializer

    def get(self,request):
        user = self.request.user 
        user_profile = Profile.objects.get(user=user) 
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data , status=status.HTTP_200_OK)

class UpdateProfileAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = UpdateProfileSerializer

    def patch(self,request,username):
        try:
            Profile.objects.get(user__username = username)
        except Profile.DoesNotExist:
            raise ProfileNotFound
        user_name = request.user.username 
        if user_name != username:
            raise NotYourProfile
        data = request.data
        serializer = UpdateProfileSerializer(instance=request.user.profile,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
