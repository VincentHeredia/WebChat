import re

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm


def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/chat')
	
	c = {}
	c.update(csrf(request))
	return render(request, 'login.html', c)
	
def invalid_login(request):
	c = {
		'hasErrors': True,
	}
	c.update(csrf(request))
	return render(request, 'login.html', c)
	
def auth_view(request):
	usernameInput = request.POST.get('name', '')
	passwordInput = request.POST.get('pass', '')
	user = auth.authenticate(username=usernameInput, password=passwordInput)
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/loggedin')
	else:
		return HttpResponseRedirect('/invalid')
	
def loggedin(request):
	return HttpResponseRedirect('/chat')
	
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login')

#Check information
def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/chat')

	c = {}
	c.update(csrf(request))

	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/register_success')
		else:
			c = {
				'hasErrors': True,
				'form': form
			}
	else:
		c['form'] = UserCreationForm()
	
	return render(request ,'register.html',c)
	
	
def register_success(request):
	return render(request, 'registerSuccess.html')
	
	
	
""" regex checking example
#regex: ^[a-zA-Z0-9]*$ 
#Matches with a string with no special characters
if not bool(re.fullmatch("[a-zA-Z0-9]*",data['user'])):
	print("Recieved invalid username")
	return #do nothing, username is invalid
"""

""" old create user methods

#create a new account
def newAccount(request):
	c = {}
	c.update(csrf(request))
	return render(request, 'createAccount.html', c)

#Error creating a new account
def register_failed(request):
	c = {
		'hasErrors': True,
	}
	c.update(csrf(request))
	return render(request, 'createAccount.html', c)


success = True
print( request.method )

form = UserCreationForm(request.POST)

username = request.POST.get('inputName', '')
password = request.POST.get('inputPassword', '')
passConfirm = request.POST.get('inputConfirmPassword', '')


if not bool(re.fullmatch("[a-zA-Z0-9]*",username)) and len(username) > 15 or len(username) < 4:
	success = False

if password == passConfirm and len(password) > 50 or len(password) < 5:
	success = False

if success is not None and form.is_valid():
	form.save()
	user = auth.authenticate(username=username, password=password)
	auth.login(request, user)
	return HttpResponseRedirect('/loggedin')
else:
	return HttpResponseRedirect('/register_failed')
"""
