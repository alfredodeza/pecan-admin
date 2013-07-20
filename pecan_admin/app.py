from pecan import make_app

from beaker.middleware import SessionMiddleware

from pecan_admin import models
from pecan_admin.templates import helpers


def setup_app(config):

    def add_middleware(app):
        options = getattr(config, 'session', {})
        return SessionMiddleware(app, **options)

    models.init_model()

    return make_app(
        config.app.root,
        static_root     = config.app.static_root,
        template_path   = config.app.template_path,
        logging         = getattr(config, 'logging', {}),
        wrap_app        = add_middleware,
        debug           = getattr(config.app, 'debug', False),
        force_canonical = getattr(config.app, 'force_canonical', True),
        hooks           = getattr(config.app, 'hooks', []),
        extra_template_vars = dict(h=helpers),
    )
