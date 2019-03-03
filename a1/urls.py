from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
	path('foo/', foo),
	path('app/', AppList.as_view()),
	path('app/<int:pk>/', AppDetail.as_view()),
]