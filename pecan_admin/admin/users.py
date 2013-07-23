from pecan_admin import models


class AdminUser(object):  # consider having a helper to inherit?

    name = 'users'
    fields = ('username',)
    model = models.users.AdminUser
