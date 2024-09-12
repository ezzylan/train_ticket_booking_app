from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Train(models.Model):
    number = models.PositiveIntegerField(unique=True)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    arrival_date = models.DateField()
    arrival_time = models.TimeField()

    def __str__(self):
        return f"Train {self.number}"


class Coach(models.Model):
    LETTER_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
        ("F", "F"),
    ]

    train = models.ForeignKey(Train, related_name="coaches", on_delete=models.CASCADE)
    letter = models.CharField(
        max_length=1,
        choices=LETTER_CHOICES,
    )

    def __str__(self):
        return f"Coach {self.letter} of Train {self.train.number}"

    def save(self, *args, **kwargs):
        if self.train.coaches.count() >= 6 and not self.pk:
            raise ValidationError(f"Train {self.train.number} can only have 6 coaches.")
        self.letter = self.letter.upper()
        super().save(*args, **kwargs)


class Seat(models.Model):
    coach = models.ForeignKey(Coach, related_name="seats", on_delete=models.CASCADE)
    booking = models.ForeignKey(
        "Booking",
        related_name="seats",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    number = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )
    is_locked = models.BooleanField(default=False)
    user_id_locked = models.PositiveIntegerField(null=True, blank=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Seat {self.coach.letter}{self.number} in Train {self.coach.train.number}"
        )

    def save(self, *args, **kwargs):
        if self.coach.seats.count() >= 20 and not self.pk:
            raise ValidationError(f"Coach {self.coach.letter} can only have 20 seats.")
        super().save(*args, **kwargs)


class Booking(models.Model):
    user = models.ForeignKey(
        "auth.User", related_name="bookings", on_delete=models.CASCADE
    )
    train = models.ForeignKey(Train, related_name="bookings", on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking by {self.user.username}"
