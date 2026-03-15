from django.urls import path

from shiftings.events.views.event import EventDetailView, EventEditView, EventListView, FutureEventsListView, \
    MyEventsListView, MyFutureEventsListView

urlpatterns = [
    path('', EventListView.as_view(), name='events'),
    path('upcoming/', FutureEventsListView.as_view(), name='future_events'),
    path('my/', MyEventsListView.as_view(), name='my_events'),
    path('my_upcoming/', MyFutureEventsListView.as_view(), name='my_future_events'),
    path('<int:pk>/', EventDetailView.as_view(), name='event'),
    path('create/<int:org_pk>/', EventEditView.as_view(), name='event_create'),
    path('<int:pk>/update/', EventEditView.as_view(), name='event_update'),
]
