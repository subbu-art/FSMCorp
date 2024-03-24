from django.test import TestCase, Client
from django.urls import reverse
from .models import Ticket, User
from .views import random_ticket_assign
class TicketTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='test123')
        self.client.login(username='testuser', password='test123')

    def test_create_ticket(self):
        response = self.client.post(reverse('ticket-create'), {
            'title': 'Test Ticket',
            'description': 'This is a test ticket.',
            'priority': 'High',
            'severity': 'High'
        })
        self.assertEqual(response.status_code, 302)  # Redirected after successful ticket creation
        self.assertTrue(Ticket.objects.filter(title='Test Ticket').exists())  # Ticket created successfully

    def test_edit_ticket(self):
        ticket = Ticket.objects.create(title='Test Ticket', description='Initial description')
        response = self.client.post(reverse('close-ticket', args=[ticket.id]), {
            'title': 'Edited Test Ticket',
            'description': 'Updated description',
            'priority': 'Medium',
            'severity': 'Low'
        })
        self.assertEqual(response.status_code, 302)  # Redirected after successful ticket edit
        edited_ticket = Ticket.objects.get(id=ticket.id)
        self.assertEqual(edited_ticket.title, 'Edited Test Ticket')
        self.assertEqual(edited_ticket.description, 'Updated description')
        self.assertEqual(edited_ticket.priority, 'Medium')
        self.assertEqual(edited_ticket.severity, 'Low')

    def test_list_tickets(self):
        Ticket.objects.create(title='Test Ticket 1', description='Description 1')
        Ticket.objects.create(title='Test Ticket 2', description='Description 2')
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, 200)  # Successfully retrieved ticket list
        self.assertEqual(len(response.context['tickets']), 2)  # Two tickets listed

    def test_assign_ticket_to_user(self):
        ticket = Ticket.objects.create(title='Test Ticket', description='Description')
        user2 = User.objects.create_user(username='testuser2', password='test456')
        # response = self.client.post(reverse('assign-ticket', args=[ticket.id]), {
        #     'assignee': user2.id
        # })
        # self.assertEqual(response.status_code, 302)  # Redirected after successful assignment
        updated_ticket = Ticket.objects.get(id=ticket.id)
        updated_ticket.assigned_to = random_ticket_assign()
        self.assertEqual(updated_ticket.assigned_to, user2)
