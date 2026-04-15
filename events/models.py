import uuid
from django.db import models, transaction
from django.db.models import Sum
from django.core.exceptions import ValidationError


class Venue(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class EventQuerySet(models.QuerySet):
    def with_available_tickets(self):
        return self.annotate(total_available_tickets=Sum('tickettype__quantity_available', default=0))


class Event(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return self.title


class TicketType(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.event.title} - {self.name}"


class OrderManager(models.Manager):
    @transaction.atomic
    def create_purchase(self, event_id, ticket_type_id, quantity, customer_email):
        event = Event.objects.get(uuid=event_id)

        ticket_type = TicketType.objects.select_for_update().get(
            uuid=ticket_type_id,
            event=event,
        )

        if ticket_type.quantity_available < quantity:
            raise ValidationError("Not enough tickets available")

        ticket_type.quantity_available -= quantity
        ticket_type.save(update_fields=['quantity_available'])

        order = self.create(
            event=event,
            customer_email=customer_email,
            status=Order.Status.CONFIRMED,
        )

        OrderLine.objects.create(
            order=order,
            ticket_type=ticket_type,
            quantity=quantity,
        )

        return order


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    customer_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    objects = OrderManager()

    def __str__(self):
        return f"Order {self.uuid} - {self.customer_email}"


class OrderLine(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='lines')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.order.uuid} - {self.ticket_type.name} x{self.quantity}"
