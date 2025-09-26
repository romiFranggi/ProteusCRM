from django.urls import path
from . import views



urlpatterns = [
    path('', views.login_supervisor, name='login_supervisor'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('snapshots/', views.snapshots_list, name='snapshots_list'),
    path('snapshots/<int:snapshot_id>/', views.snapshot_detail, name='snapshot_detail'),
    path('logout/', views.logout_view, name='logout'),
]
