from pecan import request
from pecan.hooks import PecanHook
from pecan_admin import models


class AuthenticationHook(PecanHook):
    """
    Stores the currently logged-in user in the request context.
    """

    def _get_current_user(self, session):
        if 'user_id' in session:
            return models.User.get(session['user_id'])
        else:
            return None

    def on_route(self, state):
        session = state.request.environ['beaker.session']
        request.context['user'] = self._get_current_user(session)


def save_user_session(user):
    session = request.environ['beaker.session']
    session['user_id'] = user.id
    session.save()


def remove_user_session():
    session = request.environ['beaker.session']
    session.delete()
