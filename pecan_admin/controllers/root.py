from pecan import expose, request, redirect, conf
from pecan_admin import admin, models
from pecan_admin.controllers.models import ModelController
from pecan_admin.lib.auth import save_user_session, remove_user_session


def base_admin_config():
    # XXX this needs to obviously be configurable
    # faking it for now
    return {'users': admin.users.AdminUser}

def admin_config():
    """
    Get the user configuration, and attempt to get the base_admin
    configuration in it.
    """
    config = getattr(conf, 'pecan-admin', {})
    config.setdefault('Admin Auth', base_admin_config())
    return config


class RootController(object):

    @expose(generic=True, template='index.html')
    def index(self):
        user = request.context.get('user')
        if not user:
            redirect('/login', internal=True)
        return dict(errors='', models=admin_config())

    @index.when(method='POST', template='login.html')
    def _post_login(self, *args, **kwargs):
        user = models.User.filter_by(username=kwargs['username']).first()
        if user:
            if user.validate_password(kwargs.get('password')):
                save_user_session(user)
                redirect('/')
        return dict(errors='wrong password or username', form_data=kwargs)

    @expose(template='login.html')
    def login(self):
        return dict(errors='')

    @expose()
    def logout(self):
        remove_user_session()
        redirect('/')

    @expose()
    def _lookup(self, admin_model, *remainder):
        # we need to be dynamic here and get controllers that we have been
        # configured to serve as part of the admin
        for _, group in admin_config().items():
            if admin_model in group.keys():
                return ModelController(group[admin_model]), remainder
