from django.apps import AppConfig

class WardrobeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wardrobeapp'

    def ready(self):
        import wardrobeapp.signals  # ✅ Connect signals here
