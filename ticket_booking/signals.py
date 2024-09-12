from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Train, Coach, Seat


@receiver(post_save, sender=Train)
def create_coaches_and_seats(instance, created, **kwargs):
    if created:
        for i, letter in enumerate(["A", "B", "C", "D", "E", "F"]):
            coach = Coach.objects.create(train=instance, letter=letter)

            for seat_num in range(1, 21):
                Seat.objects.create(coach=coach, number=seat_num)
