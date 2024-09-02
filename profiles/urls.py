from django.urls import path

from profiles.views import ProfileListView, ProfileDetailView, ProfileCreateView


urlpatterns = [
    path('list', ProfileListView.as_view(), name='profile_list'),
    path('detail', ProfileDetailView.as_view(), name='profile_detail'),
    path('', ProfileCreateView.as_view(), name='profile_create')
]
