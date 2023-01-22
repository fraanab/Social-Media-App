from django.shortcuts import render, redirect
from .forms import SignUpForm, UpdateProfile,PostForm
from .models import Profile, Post, LikePost, FollowersCount
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

import re

# User = get_user_model()


def frontpage(request):
	if request.user.is_authenticated:
		following_posts = []
		already_following = []

		user_following = FollowersCount.objects.filter(user=request.user.username)	#users i follow
		for user_set in user_following:												#for each in that bunch
			x = Profile.objects.filter(slug=user_set.follower)						#grab the users
			for y in x:
				for a in Post.objects.filter(user=y.id_user):						#iterate through their posts
					following_posts.append(a)										#append them to a list
		myposts = Post.objects.filter(user=request.user)							#authenticated user's posts
		for x in myposts:															#iterating through his posts
			following_posts.append(x)												#append authenticated user's posts

		following_posts.sort(key=lambda x: x.created_at, reverse=True)				#sorts by date of creation

		prof = Profile.objects.get(username=request.user)
		profiles = Profile.objects.all().order_by('-id_user')
		posts = Post.objects.all()

		# follow_suggestions = FollowersCount.objects.filter(user=request.user.username)
		not_following_users = []
		# not_following = FollowersCount.objects.filter(~Q(user=request.user.username))
		not_me = FollowersCount.objects.exclude(user=request.user.username).distinct()
		# for x in not_following:
		# 	for a in Profile.objects.filter(~Q(slug=x.follower)):
		# 		not_following_users.append(a)
		follow_suggest = []
		for a in profiles:
			follow_suggest.append(a)
		for a in user_following:
			follow_suggest.remove(Profile.objects.get(slug=a.follower))
			print(follow_suggest, request.user.username)
		follow_suggest.remove(Profile.objects.get(username=request.user))
		
		post_form = PostForm()

		context = {
			'prof':prof,
			'posts':posts,
			'profiles':profiles,
			'post_form':post_form,
			'following_posts':following_posts, 'already_following':already_following,
			'not_following_users':not_following_users, 'follow_suggest':follow_suggest
		}
		return render(request, 'frontpage.html', context)
	else:
		return redirect('login')

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)

			Profile.objects.create(username=user, slug=str(user.username), id_user=request.user.id)

			return redirect('updateprofile', user.pk)
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form':form})

@login_required
def updateprofile(request, pk):
	thisprofile = Profile.objects.get(username=request.user)
	thispk = pk

	if request.method == 'POST':
		
		if pk == thisprofile.id_user:
			thisprofile.pfp.delete()
			pfp = request.FILES.get('pfp')
			bio = request.POST.get('bio')
			# location = request.POST.get('location')

			thisprofile.pfp = pfp
			thisprofile.bio = bio
			# thisprofile.location = location
			thisprofile.save()

			print('saved', bio, request.user.id, request.user.pk, thisprofile.pfp.url)
			return redirect('profile', thisprofile.slug)
		else:
			print(f'{pk}, {thisprofile.pk}')
			return redirect('/')

	return render(request, 'updateprofile.html', {'thisprofile':thisprofile, 'thispk':thispk})
@login_required
def newpost(request):
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			newform = form.save(commit=False)
			newform.image = request.FILES.get('image')
			newform.caption = request.POST.get('caption')
			newform.save()
			Post.objects.filter(image=newform.image).update(user=request.user)
			return redirect(request.META['HTTP_REFERER'])
		else:
			print('not valid')
			return redirect('/')

@login_required
def deletepost(request, pk):
	if request.method == 'POST':
		Post.objects.get(id=pk).delete()
		return redirect('/')

@login_required
def likepost(request, id):
	if request.method == 'POST':
		username = request.user.username
		post = Post.objects.get(id=id)
		like = LikePost.objects.filter(post_id=id, username=username).first()
		if like == None:
			newlike = LikePost.objects.create(post_id=id, username=username)
			newlike.save()
			post.likes += 1
			post.save()
			return redirect(request.META['HTTP_REFERER'])
		else:
			like.delete()
			post.likes -= 1
			post.save()
			return redirect(request.META['HTTP_REFERER'])

@login_required
def profile(request, slug):
	following = []
	followers = []
	asd = ''

	profile = Profile.objects.get(slug=slug)
	profiles = Profile.objects.all()
	logged_user = Profile.objects.get(slug=request.user)

	posts = Post.objects.filter(user=profile.id_user)
	post_form = PostForm()

	followed = FollowersCount.objects.filter(follower=profile.username) 
	for user_set in followed: 
		x = Profile.objects.filter(slug=user_set.user)
		for y in x:
			followers.append(y)

	user_following = FollowersCount.objects.filter(user=profile.username)	#users i follow
	for user_set in user_following:											#for each in that bunch
		x = Profile.objects.filter(slug=user_set.follower)
		print(user_set.follower)
		for y in x:
			following.append(y)												#append to show on template

	context = {
		'profile':profile,
		'profiles':profiles,
		'logged_user':logged_user,
		'posts':posts,
		'post_form':post_form,
		'following':following,'followers':followers, 'asd':asd
	}
	return render(request, 'profile.html', context)

@login_required
def follow(request, slug):
	if request.method=='POST':
		follower = slug
		user = request.user
		if FollowersCount.objects.filter(follower=follower, user=user).first():
			FollowersCount.objects.get(follower=follower, user=user).delete()
			return redirect(request.META['HTTP_REFERER'])
		else:
			FollowersCount.objects.create(follower=follower, user=user)
			return redirect(request.META['HTTP_REFERER'])
	else:
		return redirect(request.path)

@login_required
def deleteacc(request, username, id_user):
	if request.user.is_superuser or username == request.user.username:
		if request.method == 'POST':
			Profile.objects.get(id_user=id_user).delete()
			User.objects.get(username=username).delete()
			FollowersCount.objects.get(user=username).delete()
			FollowersCount.objects.get(follower=username).delete()

			return redirect('login')
			# return HttpResponse(f'<p>{me}</p>')
	else:
		return redirect('/')