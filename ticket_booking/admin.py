from django import forms
from django.contrib import admin

from .models import Train, Coach, Seat, Booking

CITY_CHOICES = [
    (city, city)
    for city in [
        "Kuala Lumpur",
        "George Town",
        "Kota Bharu",
        "Shah Alam",
        "Kuala Terengganu",
        "Johor Bahru",
        "Ipoh",
        "Alor Setar",
        "Kuantan",
        "Melaka",
        "Putrajaya",
        "Labuan",
        "Kuching",
        "Kota Kinabalu",
    ]
]


class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = "__all__"
        widgets = {
            "origin": forms.Select(choices=CITY_CHOICES),
            "destination": forms.Select(choices=CITY_CHOICES),
        }


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    form = TrainForm


admin.site.register(Coach)
admin.site.register(Seat)
admin.site.register(Booking)
