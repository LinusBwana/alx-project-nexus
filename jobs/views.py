from django.shortcuts import render
from rest_framework import viewsets
from .serializers import IndustrySerializer, LocationSerializer, CompanySerializer, JobSerializer
from .models import Industry, Location, Company, Job
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class IndustryViewset(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    # For general keyword search
    search_fields = ['name', 'slug', 'description']


class LocationViewset(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # For general keyword search
    search_fields = ['country', 'city', 'region', 'is_remote']


class CompanyViewset(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # For general keyword search
    search_fields = ['name', 'slug', 'industry', 'locations__country', 
                     'locations__region', 'locations__city', 'description', 
                     'website_url']


class JobViewset(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    # For general keyword sear
    search_fields = ['title', 'slug', 'category__name', 'locations__country', 
                     'locations__region', 'description', 'experience_level', 
                     'requirements', 'responsibilities', 'skills_required']