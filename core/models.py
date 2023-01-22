from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Profile(models.Model):
	# username = models.CharField(max_length=100, unique=True)
	username = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	id_user = models.IntegerField()
	slug = models.SlugField(max_length=255, default=str(User.username))
	bio = models.TextField(max_length=255, blank=True, null=True)
	pfp = models.FileField(upload_to='uploads/pfp/', default='blank-pfp.png')
	# location = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return f'{self.username} with id {self.id_user}'

class Post(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	# user = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	image = models.FileField(upload_to='uploads/posts/')
	caption = models.CharField(max_length=150, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	likes = models.IntegerField(default=0)
	class Meta:
		ordering = ('-created_at',)
	def __str__(self):
		return f'{self.user}: {self.caption} ( {self.created_at} )'

class LikePost(models.Model):
	post_id = models.CharField(max_length=500)
	username = models.CharField(max_length=255)

	def __str__(self):
		return self.username

class FollowersCount(models.Model):
	follower = models.CharField(max_length=255)
	user = models.CharField(max_length=255)
	def __str__(self):
		return f'{self.user} followed {self.follower}'