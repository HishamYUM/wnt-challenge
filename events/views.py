from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Event, TicketType, Order, OrderLine
from .serializers import EventListSerializer, EventDetailSerializer, PurchaseSerializer, PurchaseResponseSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.with_available_tickets().select_related('venue')
    serializer_class = EventListSerializer
    pagination_class = PageNumberPagination


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.select_related('venue').prefetch_related('tickettype_set')
    serializer_class = EventDetailSerializer
    lookup_field = 'uuid'


class PurchaseView(APIView):
    def post(self, request, pk):
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = Order.objects.create_purchase(
                event_id=pk,
                ticket_type_id=serializer.validated_data['ticket_type_id'],
                quantity=serializer.validated_data['quantity'],
                customer_email=serializer.validated_data['customer_email'],
            )
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        except TicketType.DoesNotExist:
            return Response(
                {"error": "Ticket type not found for this event"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            return Response(
                {"error": e.message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response_serializer = PurchaseResponseSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
