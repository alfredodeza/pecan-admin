from pecan import expose


class ModelController(object):

    def __init__(self, admin_model):
        self.admin_model = admin_model
        self.model = self.admin_model.model

    @expose(template='models/index.html')
    def index(self):
        all_items = self.model.query.all()  # oh so very dangerous
        return dict(
                name=self.admin_model.name, 
                items=all_items, 
                fields=self.admin_model.fields)
