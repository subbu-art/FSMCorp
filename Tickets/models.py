from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import AbstractUser
class Ticket(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('Resolved', 'Resolved'),

    ]
    COMPLETED_REASON_CHOICES = [
        ('resolved_by_technician', 'Resolved by technician'),
        ('customer_not_available', 'Customer not available'),
        ('equipment_replaced', 'Equipment replaced'),
        ('service_completed', 'Service completed'),
        ('task_canceled_by_client', 'Task canceled by client'),
        ('duplicate_request', 'Task canceled due to duplicate request'),
        ('incorrect_information', 'Task canceled due to incorrect information'),
        ('lack_of_resources', 'Task canceled due to lack of resources'),
        ('external_factors', 'Task canceled due to external factors'),
        ('task_closed_without_resolution', 'Task closed without resolution'),
        ('transferred_to_another_team', 'Task transferred to another team'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=100,blank=True, null=True,)
    description = models.TextField(blank=True, null=True,)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=10, blank=True,null=True, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tickets', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets',blank=True,null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    completed_reason = models.CharField(max_length=100, blank=True, null=True, choices=COMPLETED_REASON_CHOICES)
    completed_at = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

