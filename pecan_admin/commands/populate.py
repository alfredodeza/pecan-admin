from pecan.commands.base import BaseCommand
from pecan import conf, load_app

from pecan_admin import models


def out(string):
    print "==> %s" % string

# This is not meant to be a pecan command as
# we want populating to be run with another app


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
    models.Base.metadata.create_all(conf.sqlalchemy.engine)
except:
    models.rollback()
    out("ROLLING BACK... ")
    raise
else:
    out("COMMITING... ")
    models.commit()
