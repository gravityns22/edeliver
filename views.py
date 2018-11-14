from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm



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

	context = {
		'title':'Home',
		'content':'Welcome to the contact page',
		'form': contact_form



	}

	return render(request, 'contact/view.html', context)

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