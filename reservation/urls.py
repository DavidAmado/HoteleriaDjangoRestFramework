from django.urls import path, include
from rest_framework import routers
from .views import ReservationViewSet, RoomViewSet, GuestViewSet, ReservationCheckIn, ReservationCheckOut, IsRoomsAviable

router = routers.DefaultRouter()
router.register(r'reservations', ReservationViewSet, basename='reservations')
router.register(r'rooms', RoomViewSet)
router.register(r'guests', GuestViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/reservations/<int:reservation_id>/checkin/', ReservationCheckIn.as_view()),
    path('api/reservations/<int:reservation_id>/checkout/', ReservationCheckOut.as_view()),
    path('api/rooms/<int:room_id>/status/', IsRoomsAviable.as_view()),
]