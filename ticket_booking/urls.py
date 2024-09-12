"""
URL configuration for train_ticket_booking_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from ticket_booking import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("trains/<int:train_number>/", views.CoachListView.as_view(), name="train"),
    path("seat/<int:seat_id>/", views.update_seat_view, name="update_seat"),
    path("payment/", views.payment_view, name="payment"),
    path("booking/<int:pk>/", views.BookingDetailView.as_view(), name="booking"),
    path("bookings/<int:user_id>/", views.BookingListView.as_view(), name="bookings"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
