
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Friends
from django.core.urlresolvers import reverse
import bcrypt
import re

# Create your views here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')
NAME = re.compile(r'[0,1,2,3,4,5,6,7,8,9]')


def index(request):
	return render (request, "index.html")

def register(request):
	if request.method == 'POST':
		user_tuple2 = User.userManager.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['pw'], request.POST['c_pw'],request.POST['alias'], request.POST['dob'])
		if user_tuple2[0]:
			request.session['id'] = user_tuple2[1].id
			request.session['name'] = user_tuple2[1].first_name + " " + user_tuple2[1].last_name
			return redirect('/friends')
		else:
			for i in user_tuple2[1]:
				messages.info( request, user_tuple2[1][i], extra_tags = 'rg')
		 	return redirect('/')

			#make user register again
	
def friends(request):

	currentuser = User.userManager.get(id = request.session['id'])
	not_friend = User.userManager.exclude(addingu__currentuser = currentuser)
	buddy = User.userManager.filter(addingu__currentuser =currentuser)
	context = {
		"cuser" : currentuser,
		"friends": buddy,
		"users" : User.userManager.exclude(id = request.session['id']),
		"not_friends" : not_friend
	}
	print not_friend
	return render (request, "index2.html", context)

def login(request):

	if request.method == 'POST':
		user_tuple = User.userManager.login(request.POST['elogin'] , request.POST['Lpw'])
		if user_tuple[0]:
			request.session['id'] = user_tuple[1].id
			request.session['name'] = user_tuple[1].first_name + " " + user_tuple[1].last_name
			#change request.session to message later or add request.session to flash message later
			return redirect('/friends')
		else:	
			for i in user_tuple[1]:
				messages.info( request, user_tuple[1][i], extra_tags = 'lg')
			return redirect('/')

def logoff(request):
	request.session.clear()
	return redirect('/')

def profile(request, id):

	user = User.userManager.get(id = id)

	context = {
		"user" : user,
	}

	return render ( request, "index3.html", context)

def addFriend(request, id):
	if request.method == "POST":
		try:
			print " I'M CHECKING 1111111111111111111111111111111"
			current = User.userManager.filter(id = request.session['id'])
			print current
			adding = User.userManager.filter(id = id)		
			print adding
			if current and adding:
				print "I JUST PASS IF STMT @@@@@@@@@@@@@@@@@@@@@"
				Friends.objects.create(currentuser = current[0], friend = adding[0])
				print "friend is added!!!!!!!!!!!!!!!!!!!"
				return redirect(reverse('friends'))
		except:
			return redirect(reverse('friends'))

def remove(request,id):
	if request.method == "GET":
		print "command coming in!!"
		try:
			print "checking for users"
			current = User.userManager.filter(id = request.session['id'])
			removing = User.userManager.filter(id = id)
			print removing
			if current and removing:
				print "starting the removing process"
				Friends.objects.filter(currentuser = current[0], friend = removing[0]).delete()
				print "Friend is removed!!! OH NOOOOOOOOOOOOOOOOO"
				return redirect(reverse('friends'))
		except:
			return redirect(reverse('friends'))



	

