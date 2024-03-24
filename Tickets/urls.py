from django.urls import path
from .views import ticket_create, ticket_list, ticket_detail, close_ticket,dashboard,ticket_list_resolved, assign_ticket,assignee_list

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('create/', ticket_create, name='ticket-create'),
    path('list/', ticket_list, name='ticket-list'),
    path('resolve-list/', ticket_list_resolved, name='ticket-list-resolve'),
    path('assignee-list/', assignee_list, name='assignee-list'),
    path('assign-ticket/<int:ticket_id>/', assign_ticket, name='assign-ticket'),
    path('close-ticket/', close_ticket, name='list-close-ticket'),
    path('close-ticket/<int:ticket_id>/', close_ticket, name='close-ticket'),
    path('<int:ticket_id>/', ticket_detail, name='ticket-detail'),
    # Add URLs for other views
]
