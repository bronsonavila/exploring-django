from django.urls import path

from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.TeamListView.as_view(), name='list'),
    path('<int:pk>/', views.TeamDetailView.as_view(), name='detail'),
    path('create/', views.TeamCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', views.TeamUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.TeamDeleteView.as_view(), name='delete'),
]
