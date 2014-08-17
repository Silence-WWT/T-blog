from django.contrib import admin
from blog.models import *

admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(BlogImg)