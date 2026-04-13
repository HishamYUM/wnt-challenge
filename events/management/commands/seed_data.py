import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from events.models import Venue, Event, TicketType, Order, OrderLine


class Command(BaseCommand):
    help = "Seed the database with sample data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        OrderLine.objects.all().delete()
        Order.objects.all().delete()
        TicketType.objects.all().delete()
        Event.objects.all().delete()
        Venue.objects.all().delete()

        venues = []
        venue_data = [
            ("Madison Square Garden", "4 Pennsylvania Plaza, New York, NY 10001", 20000),
            ("The O2 Arena", "Peninsula Square, London SE10 0DX", 20000),
            ("Staples Center", "1111 S Figueroa St, Los Angeles, CA 90015", 19000),
            ("Sydney Opera House", "Bennelong Point, Sydney NSW 2000", 5738),
            ("Red Rocks Amphitheatre", "18300 W Alameda Pkwy, Morrison, CO 80465", 9525),
        ]
        for name, address, capacity in venue_data:
            venue = Venue.objects.create(name=name, address=address, capacity=capacity)
            venues.append(venue)

        self.stdout.write(f"  Created {len(venues)} venues")

        now = timezone.now()
        events = []
        event_prefixes = [
            "Summer", "Winter", "Spring", "Autumn", "Annual", "Weekend",
            "Downtown", "Lakeside", "Rooftop", "Underground", "Late Night",
            "International", "Local", "Acoustic", "Electric", "Grand",
        ]
        event_types = [
            "Music Festival", "Tech Conference", "Comedy Night", "Jazz Session",
            "Rock Concert", "Symphony Evening", "Stand-Up Show", "Dance Party",
            "Folk Night", "Hip Hop Showcase", "Film Screening", "Poetry Slam",
            "Food & Wine Gala", "Charity Fundraiser", "Art Exhibition",
            "Blues Evening", "Opera Night", "Reggae Session", "DJ Set",
            "Theatre Performance", "Book Reading", "Open Mic Night",
        ]
        event_titles = [
            f"{prefix} {etype}"
            for prefix in event_prefixes
            for etype in event_types
        ]
        random.shuffle(event_titles)
        event_titles = event_titles[:200]

        for i, title in enumerate(event_titles):
            if i < 60:
                start = now - timedelta(days=random.randint(10, 120), hours=random.randint(1, 12))
            else:
                start = now + timedelta(days=random.randint(5, 180), hours=random.randint(1, 12))

            end = start + timedelta(hours=random.randint(2, 6))
            venue = random.choice(venues)

            event = Event.objects.create(
                title=title,
                description=f"Join us for {title.lower()}! An unforgettable experience at {venue.name}.",
                venue=venue,
                start_date=start,
                end_date=end,
            )
            events.append(event)

        self.stdout.write(f"  Created {len(events)} events")

        ticket_type_options = [
            ("General Admission", Decimal("25.00"), Decimal("75.00")),
            ("VIP", Decimal("80.00"), Decimal("200.00")),
            ("Early Bird", Decimal("15.00"), Decimal("50.00")),
        ]

        ticket_types_created = 0
        for event in events:
            num_types = random.randint(2, 3)
            selected = random.sample(ticket_type_options, num_types)
            for name, min_price, max_price in selected:
                price = Decimal(str(random.randint(int(min_price), int(max_price)))) + Decimal("0.99")
                quantity = random.randint(50, 500)
                TicketType.objects.create(
                    event=event,
                    name=name,
                    price=price,
                    quantity_available=quantity,
                )
                ticket_types_created += 1

        self.stdout.write(f"  Created {ticket_types_created} ticket types")

        sample_emails = [
            "alice@example.com",
            "bob@example.com",
            "carol@example.com",
            "dave@example.com",
            "eve@example.com",
        ]

        orders_created = 0
        past_events = [e for e in events if e.start_date < now]
        for event in past_events[:5]:
            ticket_types = list(TicketType.objects.filter(event=event))
            for _ in range(random.randint(1, 3)):
                tt = random.choice(ticket_types)
                qty = random.randint(1, 4)
                tt.quantity_available -= qty
                tt.save()
                order = Order.objects.create(
                    event=event,
                    customer_email=random.choice(sample_emails),
                    status="confirmed",
                )
                OrderLine.objects.create(
                    order=order,
                    ticket_type=tt,
                    quantity=qty,
                )
                orders_created += 1

        self.stdout.write(f"  Created {orders_created} orders")
        self.stdout.write(self.style.SUCCESS("Done!"))
