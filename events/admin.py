from django.contrib import admin
from .models import Venue, Event, TicketType, Order, OrderLine

admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(TicketType)
admin.site.register(Order)
admin.site.register(OrderLine)
