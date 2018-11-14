from django.contrib.auth import login, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import ContactForm, UserCreationForm, UserLoginForm

User = get_user_model()

def display_meta(request):
	values = request.META.items()
	#values.sort()
	html = []

	for k,v in values:
		#print(k,v)
		html.append('<tr><td>{}</td><td>{}</td></tr>'.format(k, v))

		return HttpResponse('<table>{}</table>'.format(html))
		#return HttpResponse(values)


def home_page(request):

	if request.user.is_authenticated:
		print(request.user.username)

	context = {
		'title': request.user.username +' you are Home!',
		'content':'Welcome to the contact page',
		#'form': contact_form



	}

	return render(request, 'home_page.html', context)

def about_page(request):

	context = {
		'title':'About Us',
		'content':'Welcome to the contact page',
		#'form': contact_form



	}

	return render(request, 'contact/view.html', context)

def contact_page(request):
	
	contact_form = ContactForm()
	context = {
		'title':'Contact',
		'content':'Welcome to the contact page',
		'form': contact_form

	}

	if request.method == 'POST':
		print(request.POST.get('email'))
		print(request.POST.get('first_name'))
		print(request.POST.get('first_name'))
		print(request.POST.get('message'))


	return render(request, 'contact/view.html', context)



def register(request, *args, **kwargs):

	form = UserCreationForm(request.POST or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect('/login')
		#print('user created')

	return render(request, 'accounts/register.html', {'form':form})


def user_login(request, *args, **kwargs):

	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')

		user_obj = User.objects.get(username__iexact=username)
		login(request, user_obj)
		return HttpResponseRedirect('/')
		#print('user created')

	return render(request, 'accounts/login.html', {'form':form})

