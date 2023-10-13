from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='authors')
        common_group.user_set.add(user)
        return user