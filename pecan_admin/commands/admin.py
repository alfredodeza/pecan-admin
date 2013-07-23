import os
from pecan.commands.base import BaseCommand
from pecan import conf, load_app
from pecan_admin import models


def out(string):
    print "==> %s" % string


class AdminCommand(BaseCommand):
    """
    Create a user
    """
    arguments = BaseCommand.arguments + ({
        'name': '--username',
        'help': 'Username',
        'default': False,
    },)

    def model_commit(self):
        raise RuntimeError('you need to subclass ',
                           'pecan_admin.commands.admin.AdminCommand ',
                           'and override model_commit')

    def model_start(self):
        raise RuntimeError('you need to subclass ',
                           'pecan_admin.commands.admin.AdminCommand ',
                           'and override model_start')

    def make_pass(self):
        return os.urandom(30).encode('base64')[:12]

    def run(self, _args):
        super(AdminCommand, self).run(_args)
        if not _args.username:
            out("--username is required")
            return
        out("LOADING ENVIRONMENT")
        self.load_app()
        self.model_start()
        password = self.make_pass()
        new_admin_user = models.AdminUser(
            username=_args.username,
            password=password)
        self.model_commit()
        out("generated password ==> %s" % password)


if __name__ == '__main__':
    def config_file():
        import os
        from os.path import dirname
        _file = os.path.abspath(__file__)
        parent_dir = dirname(dirname(dirname(_file)))
        return os.path.join(parent_dir, 'config.py')

    load_app(config_file())
    models.init_model()
    out("BUILDING SCHEMA")
    try:
        out("STARTING A TRANSACTION...")
        models.start()
        password = os.urandom(30).encode('base64')[:12]
        new_admin_user = models.AdminUser(
            username=_args.username,
            password=password)
        models.commit()
        out("generated password ==> %s" % password)

    except:
        models.rollback()
        out("ROLLING BACK... ")
        raise
    else:
        out("COMMITING... ")
        models.commit()

