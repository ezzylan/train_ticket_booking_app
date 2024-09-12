from django.apps import AppConfig


class TicketBookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ticket_booking"

    def ready(self):
        import ticket_booking.signals
