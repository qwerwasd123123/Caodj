from django.contrib import admin
from app01 import  models
# Register your models here.
admin.site.register(models.Img)
admin.site.register(models.User)
admin.site.register(models.Blog)
admin.site.register(models.Fanstoeach)
admin.site.register(models.Suberror)
admin.site.register(models.Classify)
admin.site.register(models.Label)
admin.site.register(models.Word)
admin.site.register(models.WordToLable)