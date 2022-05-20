# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render, redirect

from myprofile.models import UserProfile
from myprofile.forms import UserProfileEditForm, UserEditForm

from common.drf import CustomRetrieveUpdateDestroyAPIView, CustomListAPIView, CustomPermission
from django_filters.rest_framework import DjangoFilterBackend



def profile(request):
    return render(request, 'myprofile/detail.html')


def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        user_profile_form = UserProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect("myprofile:detail")
    else:
        user_form = UserEditForm(instance=request.user)
        user_profile_form = UserProfileEditForm(instance=request.user.profile)

    return render(request,
                  'myprofile/edit.html',
                  {'user_form': user_form,
                   'user_profile_form': user_profile_form})


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        userprofile = UserProfile(user=user)
        userprofile.save()


class UserList(CustomListAPIView):
    """
    List all instances.
    """
    model = User
    exclude = ('password',)
    filter_fields = ('username',)
    search_fields = ('username',)
    permission_classes = [CustomPermission]


class UserDetail(CustomRetrieveUpdateDestroyAPIView):
    """
    Show / Update / Delete one instance.
    """
    model = User
    exclude = ('password',)
    permission_classes = [CustomPermission]


# Exemple
# class UserList(CustomListCreateAPIView):
#     """
#     List all instances, or create a new one.
#     """
#     model = User
#     fields = None
#     depth = 2
#     exclude = ('password',) 
#     filter_fields = ('username',)
#     search_fields = ('username',)
#     permission_classes = [CustomPermission]