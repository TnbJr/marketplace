from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.views.generic.detail import DetailView
from .models import Profile
from .forms import ProfileForm
# from reviews.models import UserReview
from django.contrib.auth import logout
# Create your views here.


class ProfileDetailView(DetailView):

	model = Profile
	

	# def get(self, request, pk):
	# 	profile = get_object_or_404(Profile, pk=pk)
	# 	user_review = UserReview.objects.filter(user=profile.user)
	# 	context={
	# 		'profile': profile,
	# 		'user_review': user_review
	# 	}
	# 	return render(request, "profile/profile_detail.html", context)

# class ProfileUpdateView(View):
# 	def get(self, request):
# 		profile = get_object_or_404(Profile, user=request.user)
# 		context = {
# 			'form': ProfileForm(instance=profile),
# 			'profile': profile
# 		}
# 		return render(request, "profile/profile_update.html", context)
	
# 	def post(self, request):
# 		profile = get_object_or_404(Profile, user=request.user)
# 		form = ProfileForm(data=request.POST or None, instance=profile)
# 		if form.is_valid():
# 			instance = form.save(commit=False)
# 			instance.save()
# 			return redirect('profile:detail', pk=profile.id)
# 		context = {
# 			'form': ProfileForm(instance=profile)
# 		}
# 		return render(request, "profile/profile_detail.html", context)

# class ProfileDeleteView(View):
# 	template = "profile/profile_delete.html"
# 	def get(self, request):
# 		context ={
# 			"title": "Delete Your Account"
# 		}
# 		return render(request, self.template, context)
# 	def post(self, request):
# 		profile = get_object_or_404(Profile, user=request.user)
# 		profile.user.is_active = False
# 		profile.user.save()
# 		logout(request)
# 		return redirect('sitemaps:index') 
