from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        from django.conf import settings
        import mongoengine

        if getattr(settings, "MONGODB_URI", ""):
            mongoengine.connect(host=settings.MONGODB_URI)
        else:
            mongoengine.connect(
                db=settings.MONGODB_DB,
                host=settings.MONGODB_HOST,
                port=settings.MONGODB_PORT,
            )
