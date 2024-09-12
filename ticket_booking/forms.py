from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit
from django.urls import reverse


class BookingForm(forms.Form):
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

    origin = forms.ChoiceField(
        label="Origin",
        choices=CITY_CHOICES,
        required=True,
    )
    destination = forms.ChoiceField(
        label="Destination",
        choices=CITY_CHOICES,
        required=True,
    )
    departure_date = forms.DateField(
        label="Departure Date",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True,
    )
    return_date = forms.DateField(
        label="Return Date",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {
            "hx_post": reverse("index"),
            "hx_swap": "outerHTML",
            "hx_target": "#trains",
        }

        self.helper.layout = Layout(
            Div("origin", "destination", css_class="d-flex gap-4"),
            Div("departure_date", "return_date", css_class="d-flex gap-4"),
            Submit("submit", "Find Trains"),
        )
