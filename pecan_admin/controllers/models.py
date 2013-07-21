from pecan import expose

class ModelController(object):

    def __init__(self, admin_model, model):
        self.admin_model = admin_model
        self.model = model

    @expose(template='models/edit.html')
    def index(self):
        return dict(
                name=self.admin_model.name,
                model=self.model,
                fields=self.model.as_dict().keys())  # XXX come on now, so lazy


class ModelsController(object):

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

    @expose()
    def _lookup(self, _id, *remainder):
        model = self.model.get(int(_id))
        if model:
            return ModelController(self.admin_model, model), remainder
