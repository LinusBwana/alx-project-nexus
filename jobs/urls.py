from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndustryViewset, LocationViewset, CompanyViewset, JobViewset

router = DefaultRouter()
router.register(r'industries', IndustryViewset, basename='industries')
router.register(r'locations', LocationViewset, basename='locations')
router.register(r'companies', CompanyViewset, basename='companies')
router.register(r'jobs', JobViewset, basename='jobs')

urlpatterns = [
    path('api/', include(router.urls)),
]