from django.urls import path
from . import views

app_name = 'petitions'

urlpatterns = [
    path('', views.index, name='index'),  # Use index as the root
    path('new/', views.create_petition, name='create_petition'),
    path('<int:petition_id>/vote/', views.vote_petition, name='vote_petition'),
]