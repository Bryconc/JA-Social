from django import forms
from django.contrib.auth.models import User

from datetime import datetime

import hashlib
import random

class UserForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': "A user with that username already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }
    username = forms.RegexField(label="Username", max_length=30,
                                regex=r'^[\w]+$',
                                help_text=r"Required. 30 characters or fewer. Letters, digits and _ only.",
                                error_messages={'invalid': r"This value may contain only letters, numbers and _ characters."})
    email = forms.EmailField(label="Email", max_length=256)
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])

        #
        # Assistance for generating activation key from: http://stackoverflow.com/questions/24935271/django-custom-user-email-account-verification
        #

        # salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        # usernamesalt = self.cleaned_data["username"]
        # user.activation_key=hashlib.sha1(salt+usernamesalt).hexdigest()
        # user.key_expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")

        if commit:
            user.save()
        return user

    # def sendEmail(self, datas):
    #     link="http://yourdomain.com/activate/"+datas['activation_key']
    #     c=Context({'activation_link':link,'username':datas['username']})
    #     f = open(MEDIA_ROOT+datas['email_path'], 'r')
    #     t = Template(f.read())
    #     f.close()
    #     message=t.render(c)
    #     #print unicode(message).encode('utf8')
    #     send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)
