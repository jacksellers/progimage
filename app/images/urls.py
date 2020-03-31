from django.urls import path

from images import views


app_name = 'images'

urlpatterns = [
    path('upload/', views.CreateImageView.as_view(), name='upload'),
    path('<code>/', views.RetrieveUpdateImageView.as_view(), name='download')
]
