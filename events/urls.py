from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.EventListView.as_view(), name='event-list'),
    path('events/<uuid:uuid>/', views.EventDetailView.as_view(), name='event-detail'),
    path('events/<uuid:pk>/purchase/', views.PurchaseView.as_view(), name='event-purchase'),
]
