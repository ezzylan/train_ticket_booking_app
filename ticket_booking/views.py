from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from .forms import BookingForm
from .models import Booking, Coach, Seat, Train

from django.contrib.auth.mixins import LoginRequiredMixin

# from django.contrib.auth.decorators import login_required


def index_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            origin = form.cleaned_data["origin"]
            destination = form.cleaned_data["destination"]
            departure_date = form.cleaned_data["departure_date"]
            return_date = form.cleaned_data["return_date"]
            # number_of_pax = form.cleaned_data["number_of_pax"]

            # Booking.objects.create(
            #     number_of_pax=number_of_pax,
            # )

            return render(
                request,
                "ticket_booking/trains.html",
                {
                    "trains": Train.objects.filter(
                        origin=origin,
                        destination=destination,
                        departure_date=departure_date,
                        arrival_date=return_date,
                    ),
                    "origin": origin,
                    "destination": destination,
                },
            )

    else:
        form = BookingForm()

    return render(request, "ticket_booking/index.html", {"form": form})


class CoachListView(ListView):
    model = Coach
    context_object_name = "coaches"
    template_name = "ticket_booking/train.html"

    def get_queryset(self):
        train = get_object_or_404(
            Train,
            number=self.kwargs.get("train_number"),
        )

        return Coach.objects.filter(train=train).prefetch_related("seats")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["train_number"] = self.kwargs["train_number"]

        train = get_object_or_404(
            Train,
            number=self.kwargs.get("train_number"),
        )

        context["origin"] = train.origin
        context["destination"] = train.destination

        user = self.request.user
        selected_seats = Seat.objects.filter(
            is_locked=True, user_id_locked=user.id
        ).values_list("coach__letter", "number")

        context["selected_seats"] = [
            f"{letter}{number}" for letter, number in selected_seats
        ]
        return context


@csrf_exempt
def update_seat_view(request, seat_id):
    user = request.user

    if not user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)

    seat = get_object_or_404(Seat, id=seat_id)

    if seat.is_locked and seat.user_id_locked == user.id:
        seat.is_locked = False
        seat.user_id_locked = None
    elif not seat.is_locked:
        seat.is_locked = True
        seat.user_id_locked = user.id

    seat.save()

    # selected_seats = Seat.objects.filter(
    #     is_locked=True, user_id_locked=user.id
    # ).values_list("id", flat=True)

    # print(list(selected_seats))

    return render(
        request,
        "ticket_booking/seat.html",
        {"seat": seat},
    )


@csrf_exempt
def payment_view(request):
    user = request.user

    selected_seats = Seat.objects.filter(is_locked=True, user_id_locked=user.id)

    SEAT_PRICE = 2
    total_amount = selected_seats.count() * SEAT_PRICE

    print(selected_seats.first())

    booking = Booking.objects.create(
        user=user,
        train=selected_seats.first().coach.train,
        total_amount=total_amount,
    )

    selected_seats.update(
        booking=booking, is_locked=False, user_id_locked=None, is_booked=True
    )

    return HttpResponseRedirect(reverse("booking", user.id))


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    context_object_name = "bookings"
    template_name = "ticket_booking/bookings.html"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class BookingDetailView(DetailView):
    model = Booking
    context_object_name = "booking"
    template_name = "ticket_booking/booking.html"


@require_POST
def login_view(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("index"))
    else:
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Invalid username or password.", status=401)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
