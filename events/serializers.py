from rest_framework import serializers
from .models import Event, TicketType, Order, Venue


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['uuid', 'name', 'price', 'quantity_available']


class EventListSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    total_available_tickets = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"

    def get_total_available_tickets(self, obj):
        total = 0
        for ticket_type in obj.tickettype_set.all():
            total += ticket_type.quantity_available
        return total


class EventDetailSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    ticket_types = TicketTypeSerializer(source='tickettype_set', many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['uuid', 'title', 'description', 'venue_name', 'start_date', 'end_date', 'ticket_types']


class PurchaseSerializer(serializers.Serializer):
    ticket_type_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)
    customer_email = serializers.EmailField()
