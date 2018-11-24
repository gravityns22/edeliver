from django import forms

from django.contrib.auth.forms import ReadOnlyPasswordHashField


from django.core.validators import RegexValidator
from .models import USERNAME_REGEX 

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Document

#import our user
from django.contrib.auth import get_user_model, authenticate
User = get_user_model()
#from .models import User <-- Above is better than using this method to import user


class UserLoginForm(forms.Form):
	"""docstring for ClassName"""


	username = forms.CharField(label='Username', validators=[
        RegexValidator(regex= USERNAME_REGEX,
                       message = 'Username must be Alphanumeric or any of the following: ". @ + -"')])
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		#second way to authenticate
		# the_user = authenticate(username=username, password=password)
		# if not the_user:
		# 	raise forms.ValidationError('Invalid credentials')
		

		
		
		#first way to authenticate
		user_object = User.objects.filter(username=username).first()
		if not user_object:
			raise forms.ValidationError('Invalid credentials -- invalid username')
		else:
			# log auth tries
			if not user_object.check_password(password):
				raise forms.ValidationError('Invalid credentials -- invalid password')
		return super(UserLoginForm,self).clean(*args, **kwargs)

	# def clean_username(self):
	# 	username = self.cleaned_data.get('username')
	# 	user_qs = User.objects.filter(username=username).exists()
	# 	user_exists = user_qs.exists()
	# 	if not user_exists and user_qs.count() !=1:
	# 		raise forms.ValidationError('Invalid credentials')
	# 	return username

class ContactForm(forms.Form):

	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.EmailField()
	message = forms.CharField(widget=forms.Textarea)


class UserCreationForm(forms.ModelForm):
    """A form for creating new usters. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


'''
This form is used by a user to upload a csv file containing addresses
'''
def validate_file_extension(value):
        if not value.name.endswith('.csv'):
            #raise forms.ValidationError("Only CSV files are accepted")

            raise ValidationError(
            _('%(value)s is not an acceptable file format. Only CSV files are accepted'),
            params={'value': value},
        )

class UploadFileForm(forms.Form):
 	title = forms.CharField(max_length=50)
 	file = forms.FileField(validators=[validate_file_extension])


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'document', )
        exclude = ['user']

    def clean(self):
    	data = self.cleaned_data
    	print('DocumentForm--->clean:',data['document'])
    	if not str(data['document']).endswith('.csv'):
            #raise forms.ValidationError("Only CSV files are accepted")

            raise ValidationError('Must be a CSV file')