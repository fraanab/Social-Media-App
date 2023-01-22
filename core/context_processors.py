from .models import Profile
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def userprofile(request):
	if request.user.is_authenticated:
		prof = Profile.objects.get(username=request.user)

		user_search = Profile.objects.all().order_by('-id_user')
		query = request.GET.get('query', '')
		if query:
			user_search = Profile.objects.filter(Q(slug__icontains=query))
	else:
		prof = Profile.objects.get(id_user=0)
		user_search = Profile.objects.all()
	return {'thisprofile':prof, 'user_search':user_search}