import os
from pecan.commands.base import BaseCommand
from pecan import conf
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

    def make_pass(self):
        return os.urandom(30).encode('base64')[:12]

    def run(self, _args):
        super(AdminCommand, self).run(_args)
        if not _args.username:
            out("--username is required")
            return
        out("LOADING ENVIRONMENT")
        self.load_app()
        models.start()
        password = self.make_pass()
        new_invite = models.User(
                username=_args.username,
                password=password)
        models.commit()
        out("generated password ==> %s" % password)
