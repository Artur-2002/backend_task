from django.urls import path
from .views import *


urlpatterns = [
	path('images/', ImageView.as_view()),
	path('images/<int:pk>/', ImageView.as_view()),
	path('images/<int:pk>/resize/', ImageResizeView.as_view()),
]