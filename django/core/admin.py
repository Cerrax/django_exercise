from django.apps import apps
from django.contrib import admin

# Register your models here.
def autoregister(app_name):  # pragma: no cover
    app_config = apps.get_app_config(app_name)
    for model in app_config.models.values():
        try:
            admin.site.register(model)
        except AlreadyRegistered:
            pass


autoregister('core')