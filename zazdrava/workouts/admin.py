from django.contrib import admin
from .models import Workout, Session, Lap, Record, HRZone, PowerZone


admin.site.register(Workout)
admin.site.register(Session)
admin.site.register(Lap)
admin.site.register(Record)
admin.site.register(HRZone)
admin.site.register(PowerZone)
