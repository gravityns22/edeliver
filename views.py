from django.contrib.auth import login, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import ContactForm, UserCreationForm, UserLoginForm, UploadFileForm
import logging
from django.contrib import messages
from django.urls import reverse

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

def handle_uploaded_file(f):
    with open('test.csv', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			handle_uploaded_file(request.FILES['file'])
			return HttpResponseRedirect('/')
	else:
		form = UploadFileForm()

	return render(request, 'geocodeaddresses/upload.html', {'form': form})

def upload_csv(request):

	
	
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():

			try:
				csv_file = request.FILES["file"]
				handle_uploaded_file(request.FILES['file'])
				print(request.FILES)
				if not csv_file.name.endswith('.csv'):
					messages.error(request,'File is not CSV type')
					return HttpResponseRedirect('/')
			
			#if file is too large, return
				if csv_file.multiple_chunks():
					messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
					return HttpResponseRedirect('/')
				
				file_data = csv_file.read().decode("utf-8")
				
				lines = file_data.split("\n")
				#loop over the lines and save them in db. If error , store as string and then display
				for line in lines:
					print(line)
					messages.info(request, 'Three credits remain in your account.')
					logging.getLogger("error_logger").error(line)
				
				return HttpResponseRedirect('/')
				
			except Exception as e:
				logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
				messages.error(request,"Unable to upload file. "+repr(e))

	else:
		form = UploadFileForm()

	context = {
		'title': request.user.username +' you are Home!',
		'content':'Welcome to the contact page',	
		'form': form,



	}

	return render(request, 'geocodeaddresses/upload.html', context)