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
router.register(r"category/review/",views.AllCategoryReview,basename="CategoryReview")

urlpatterns = [
    path('category/filter',views.categoryfilter),
    path('review/', views.review_create),
    path('review/age',views.review_age),
    path('review/<int:review_pk>/',views.review_command),
    path('review/like/',views.review_like),
    path('like',views.like_book),
    path('mylike',views.mylike),
    path('review_orderby_date',views.review_orderby_date),
    path('review_filter', views.bookfilter),
    path('filter_by_score_and_count', views.filter_by_score_and_count)
] + router.urls
