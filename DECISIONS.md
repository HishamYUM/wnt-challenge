- **What:** Replaced `Event.objects.all()` with `select_related('venue')` in `EventListView` and `EventDetailView`.
  **Why:** Resolves N+1 queries when accessing the related venue field within serializers.
- **What:** Used `prefetch_related('tickettype_set')` on `EventDetailView`.
  **Why:** Prevents N+1 queries when accessing the list of ticket types for an event detail endpoint.
- **What:** Removed `SerializerMethodField` and `get_total_available_tickets` from `EventListSerializer` in favor of computing it in database via annotation (`total_available_tickets`).
  **Why:** Resolves an N+1 code smell and pushes analytical aggregation to the ORM directly.
- **What:** Substituted explicit `fields` enumeration for `"__all__"` in `EventListSerializer`.
  **Why:** Secures API contract structure and prevents accidental field leakage.
- **What:** Applied explicit `PageNumberPagination` to the `EventListView`.
  **Why:** Protects bulk endpoints from OOM vulnerability by paginating lists instead of responding with full datasets.
- **What:** Abstracted transactional purchase state manipulation to `OrderManager.create_purchase()`.
  **Why:** Ensures models and managers hold business logic, keeping Views purely for HTTP traffic orchestration.
- **What:** Executed `.select_for_update()` on tickets within a `@transaction.atomic()` manager layer.
  **Why:** Mitigates check-then-decrement race conditions during high-volume purchasing scenarios by placing table locks.
- **What:** Transferred JSON instantiation out of `PurchaseView` into a dedicated `PurchaseResponseSerializer`.
  **Why:** Standardizes endpoint egress validation payload shapes rather than manually curating nested Python dict strings inside controller logic.
- **What:** Added `models.TextChoices` to the `Order` model representing possible status limits.
  **Why:** Swaps loose raw strings for encapsulated validation rules across standard schema usage scopes natively supported by ORMs.
