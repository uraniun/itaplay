import json

from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest

from utils.EmailService import EmailSender
from authentication.models import AdviserInvitations, AdviserUser
from authentication.forms import UserRegistrationForm, UserInvitationForm


def validate_verification_code(func):
    """
    Decorator that check is verification code valid, existing and open
    :param func: function, that be wrapped
    :return: nothing
    """
    def wrapper(self, request, *args, **kwargs):
        """
        Wrapper, that checks verification code
        :param self:
        :param request:
        :param args:
        :param kwargs:
        :return: BadRequest when verification code is incorrect or function in other case
        """
        verification_code = request.GET.get("code", "")

        if verification_code:
            invitation_query = AdviserInvitations.objects.filter(verification_code=verification_code)
            if invitation_query.exists():
                invitation = invitation_query.first()

                if not invitation.is_active:
                    return HttpResponseBadRequest("Invitation is already used")
            else:
                return HttpResponseBadRequest("No open invitation")
        else:
            return HttpResponseBadRequest("Invalid code")
        return func(self, request, *args, **kwargs)
    return wrapper


class RegistrationView(View):
    """
    View used for handling registration
    """

    @validate_verification_code
    def get(self, request):
        """
        Handling GET method
        :param request: Request to View
        :return: rendered registration page
        """
        return render(request, "register.html")

    @validate_verification_code
    def post(self, request):
        """
        Handling GET method
        :param request: Request to View
        :return: HttpResponse with code 201 if user is created or
        HttpResponseBadRequest if request contain incorrect data
        """
        verification_code = request.GET.get("code", "")

        invitation = AdviserInvitations.get_invitation(verification_code)

        user_registration_form = UserRegistrationForm(json.loads(request.body))

        if not user_registration_form.is_valid():
            return HttpResponseBadRequest("Invalid input data. Please edit and try again.")

        AdviserUser.create_user(user_registration_form, invitation)

        invitation.close_invitation()

        return HttpResponse(status=201)


class InviteView(View):
    """View that handles user invitation"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(InviteView, self).dispatch(*args, **kwargs)

    def post(self, request):
        """Handling GET method
            :param request: Request to View
            :return: HttpResponse with code 201 if user is invited or
                     HttpResponseBadRequest if request contain incorrect data
        """
        invite_form = UserInvitationForm(json.loads(request.body))

        if not invite_form.is_valid():
            return HttpResponseBadRequest("Invalid input data. Please edit and try again.")

        if AdviserUser.objects.filter(user__email=invite_form.data[u'email']).exists():
            return HttpResponseBadRequest("User with this e-mail is registered")

        if AdviserInvitations.objects.filter(email=invite_form.data[u'email']).exists():
            return HttpResponseBadRequest("User with this e-mail is already invited")

        sender = EmailSender(invite_form.data[u'email'])
        sender.send_invite(invite_form.data[u'id_company'])
        return HttpResponse(status=201)

    def get(self, request):
        """
        Handling GET method
            :param request: Request to View
            :return: rendered inviting page
        """
        return render(request, "invite.html")


class LoginView(View):

    def post(self, request):
        data = json.loads(request.body)

        username = data.get('username', None)
        password = data.get('password', None)

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponse(status=200)

        else:
            return HttpResponseBadRequest("incorrect username or password", status=401)

        #else:
        return HttpResponseBadRequest(status=400)

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


class LogoutView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LogoutView, self).dispatch(*args, **kwargs)

    def get(self, request, format=None):
        auth.logout(request)
        return redirect('/')