from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from api import views
from django.urls import path, include


router = DefaultRouter(trailing_slash=False)
router.register(r"books",views.BookViewSet,basename="books")
router.register(r"category",views.CategoryViewSet,basename="categorys")

urlpatterns = [
    path('review/<int:id>/', views.review),
] + router.urls
