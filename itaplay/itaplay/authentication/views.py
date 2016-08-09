from django.shortcuts import render
from django.utils import timezone

from forms import UserForm
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest

from . import models


# rewrite using class
def close_invitation(invitation):
    invitation.isActive = False
    invitation.usedTime = timezone.now()
    invitation.save()

def get_invitation(verification_code):
    if models.AdviserInvitations.objects.filter(verificationCode=verification_code).exists():
        invitation = models.AdviserInvitations.objects.get(verificationCode=verification_code)

        if not invitation.isActive:
            raise IndexError("Invitation is already used")
    else:
        raise IndexError("No open invitation")
    return invitation


def register(request):
    verification_code = request.GET.get("code", "")

    if verification_code:
        try:
            invitation = get_invitation(verification_code)
        except IndexError as e:
            return HttpResponseBadRequest(e.message)
    else:
        return HttpResponseBadRequest("Invalid code")

    if request.method == 'POST':
        base_form = UserForm(request.POST)

        if not base_form.is_valid():
            return HttpResponseBadRequest("Invalid input data. Please edit and try again.")

        new_base_user = base_form.save(commit=False)
        new_base_user.username = invitation.email
        new_base_user.email = invitation.email
        new_base_user.save()

        new_extended_user = models.AdviserUser()
        new_extended_user.setup_user(new_base_user, invitation)
        new_extended_user.save()

        close_invitation(invitation)

        return HttpResponseRedirect("/")

    return render(request, "register.html")
