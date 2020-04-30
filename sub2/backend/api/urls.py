from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from api import views
from django.urls import path, include


router = DefaultRouter(trailing_slash=False)
router.register(r"books",views.BookViewSet,basename="books")
router.register(r"book/(?P<id>.+)",views.BookDetailViewSet,basename="book")
router.register(r"category",views.CategoryViewSet,basename="categorys")
router.register(r"likecategory",views.LikeCategoryViewSet,basename="likecategory")
router.register(r"author",views.AuthorViewSet,basename="author")
router.register(r"reviews",views.ReviewViewSet,basename="review")

urlpatterns = [
    path('review/', views.review_create),
    path('review/<int:review_pk>/',views.review_command),
    path('like',views.like_book),
    path('mylike',views.mylike),
] + router.urls
