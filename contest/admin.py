from django.contrib import admin

from .models import Administrator
from .models import Contest
from .models import Video
from .models import Competitor


# Register your models here.
admin.site.register(Administrator)
admin.site.register(Contest)
admin.site.register(Video)
admin.site.register(Competitor)