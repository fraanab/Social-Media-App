from django.urls import path, include
from .views import frontpage, signup, updateprofile, newpost, deletepost,likepost, profile, follow, deleteacc
from django.contrib.auth import views

urlpatterns = [
	path('', frontpage, name='frontpage'),
	path('signup/', signup, name='signup'),
	path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('updateprofile/<int:pk>/', updateprofile, name='updateprofile'),
	path('newpost', newpost, name='newpost'),
	path('delete/<str:pk>/', deletepost, name='deletepost'),
	path('deleteacc/<str:username>/<int:id_user>/', deleteacc, name='deleteacc'),
	path('like/<str:id>/',likepost,name='likepost'),
	path('profile/<slug:slug>/', profile, name='profile'),
	path('follow/<slug:slug>/', follow, name='follow'),
]