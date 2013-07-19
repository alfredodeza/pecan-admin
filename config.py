from pecan.hooks import TransactionHook, RequestViewerHook
from pecan_admin import models
from pecan_admin.lib.auth import AuthenticationHook

# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'pecan_admin.controllers.root.RootController',
    'modules': ['pecan_admin'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/pecan_admin/templates',
    'debug': True,
    'hooks': [
        TransactionHook(
            models.start,
            models.start_read_only,
            models.commit,
            models.rollback,
            models.clear
        ),
        RequestViewerHook({'blacklist': ['/p/']}),
        AuthenticationHook(),
    ],
    'errors': {
        '__force_dict__': True
    }
}

logging = {
    'loggers': {
        'pecan_admin': {'level': 'DEBUG', 'handlers': ['console']}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        }
    }
}

# FIXME: I need a real databasssss
sqlalchemy = {
    'url': 'sqlite:////tmp/test.db',
    'echo'          : True,
    'echo_pool'     : True,
    'pool_recycle'  : 3600,
    'encoding'      : 'utf-8'
}
