from pecan import expose, request, redirect, secure
from pecan.ext.wtforms import with_form
from pecan_admin import models
from pecan_admin.lib.auth import save_user_session, remove_user_session
from pecan_admin.forms.login import LoginForm

from pecan_admin.controllers.users import UsersController


class RootController(object):

    @expose(generic=True, template='index.html')
    def index(self):
        user = request.context.get('user')
        if not user:
            redirect('/signin', internal=True)
        return dict()

    @index.when(method='POST', template='index.html')
    @with_form(LoginForm)
    def _post_login(self, *args, **kwargs):
        # XXX doing it wrong
        form = request.pecan.get('form')
        if form:
            if getattr(form, 'errors'):
                request.context['errors'] = form.errors
                return dict(form_data=form.data, errors=form.errors)

        user = models.User.filter_by(username=kwargs['username']).first()
        save_user_session(user)
        redirect('/')

    @expose(template='signin.html')
    def signin(self):
        return dict()

    @expose()
    def logout(self):
        remove_user_session()
        redirect('/')

    @expose()
    def _lookup(self, controllers, *remainder):
        # we need to be dynamic here and get controllers that we have been
        # configured to serve as part of the admin
        pass