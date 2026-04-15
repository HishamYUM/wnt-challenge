from rest_framework import serializers
from .models import Event, TicketType, Order, Venue


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ['uuid', 'name', 'price', 'quantity_available']


class EventListSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='venue.name', read_only=True)
    total_available_tickets = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = ['uuid', 'title', 'description', 'venue_name', 'start_date', 'end_date', 'total_available_tickets']


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


class PurchaseResponseSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(source='uuid')
    event = serializers.CharField(source='event.title')
    ticket_type = serializers.SerializerMethodField()
    quantity = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id', 'event', 'ticket_type', 'quantity', 'total_price', 'status']

    def get_ticket_type(self, obj):
        line = obj.lines.first()
        return line.ticket_type.name if line else None

    def get_quantity(self, obj):
        line = obj.lines.first()
        return line.quantity if line else 0

    def get_total_price(self, obj):
        line = obj.lines.first()
        return str(line.ticket_type.price * line.quantity) if line else "0.00"
