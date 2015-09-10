from django.contrib import admin

from .models import Administrator
from .models import Contest
from .models import Video

# Register your models here.
admin.site.register(Administrator)
admin.site.register(Contest)
admin.site.register(Video)