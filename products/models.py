"""
Product documents stored in MongoDB (mongoengine).
"""
from django.utils import timezone
from mongoengine import DateTimeField, Document, FloatField, IntField, StringField


class Product(Document):
    meta = {
        "collection": "products",
        "ordering": ["-created_at"],
    }

    name = StringField(required=True, max_length=200)
    price = FloatField(required=True, min_value=0)
    quantity = IntField(required=True, min_value=0)
    # Relative path under MEDIA_ROOT, e.g. products/uuid.jpg
    image = StringField(max_length=500)
    created_at = DateTimeField(default=timezone.now)
