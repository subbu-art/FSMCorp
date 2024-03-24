import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import TicketForm, TicketCloseForm,TicketCloseFormEngineer,TicketFormCreate, TicketAssignForm
from .models import Ticket
from datetime import datetime, timedelta
from django.db.models import Q

# Get the current date
current_date = datetime.now().date()

# Add two days to the current date
future_date = current_date + timedelta(days=2)

def random_ticket_assign():
    user = User.objects.filter(is_superuser=False,is_active=True).order_by('?').first()
    return user


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketFormCreate(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            if not form.instance.deadline:
                form.instance.deadline = future_date
            # form.instance.status = "active"
            form.save()
            return redirect('ticket-list')
    else:

        form = TicketForm()
    users = User.objects.filter(is_superuser=False, is_active=True,is_staff=True)
    return render(request, 'ticket_create.html', {'form': form,"users":users})


@login_required
def ticket_list(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.order_by('-status')
    else:
        tickets = Ticket.objects.filter(Q(Q(created_by=request.user)| Q(assigned_to=request.user))).order_by('-status')
    # Filter tickets based on status, priority, etc.
    return render(request, 'ticket_list.html', {'tickets': tickets})

@login_required
def ticket_list_resolved(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.filter(status='resolved').order_by('-status')
    else:
        tickets = Ticket.objects.filter(status='resolved').filter(Q(Q(created_by=request.user)| Q(assigned_to=request.user))).order_by('-status')
    # Filter tickets based on status, priority, etc.
    return render(request, 'ticket_list.html', {'tickets': tickets})
@login_required
def assignee_list(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.filter(status='pending')
    else:
        tickets = Ticket.objects.filter(Q(Q(created_by=request.user)| Q(assigned_to=request.user))).order_by('-status')
    # Filter tickets based on status, priority, etc.
    return render(request, 'ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)

    # Render ticket details page
    return render(request, 'ticket_detail.html', {'ticket': ticket})


# Add views for closing tickets, adding notes, etc.
@login_required
def close_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    restricted_users = ['engineer1']
    if request.method == 'POST':
        if not request.user.is_superuser:
            if 'notes' in request.POST:
                form = TicketCloseFormEngineer(request.POST, instance=ticket)
            else:
                form = TicketCloseFormEngineer(instance=ticket)
            if form.is_valid():
                form.instance.status = "completed"
                form.save()
                return redirect('ticket-list')
        else:
            if 'completed_reason' in request.POST:
                form = TicketCloseForm(request.POST, instance=ticket, restricted_users=restricted_users)
            else:
                form = TicketCloseForm(instance=ticket, restricted_users=restricted_users)
            if form.is_valid():
                if form.instance.completed_reason:
                    form.instance.completed_at = datetime.now()
                form.save()
                return redirect('ticket-list')
    else:
        if not request.user.is_superuser:
            form = TicketCloseFormEngineer(instance=ticket)
        else:
            form = TicketCloseForm(instance=ticket, restricted_users=restricted_users)
    return render(request, 'close_ticket.html', {'form': form, 'ticket': ticket})

@login_required
def assign_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        if request.user.is_superuser:
            if 'assigned_to' in request.POST:
                form = TicketAssignForm(request.POST, instance=ticket)
            else:
                form = TicketAssignForm(instance=ticket)
            if form.is_valid():
                form.instance.status = "active"
                form.save()
                return redirect('ticket-list')
            else:
                return render(request, 'assign_ticket.html', {'form': form, 'ticket': ticket})
    else:
        form = TicketAssignForm(instance=ticket)
    return render(request, 'assign_ticket.html', {'form': form, 'ticket': ticket})


@login_required
def dashboard(request):
    # Retrieve and filter task data
    if request.user.is_superuser:
        assignee = request.GET.get('assignee')
        deadline = request.GET.get('deadline')
        creation_date = request.GET.get('creation_date')
        complete_reason = request.GET.get('complete_reason')
        completed_at = request.GET.get('completed_at')

        created_tasks = Ticket.objects.order_by('-status')
        total_tasks = created_tasks.count()
        completed_tasks = created_tasks.filter(status='completed').count()
        active_tasks = created_tasks.filter(status='active').count()
        flag = True

        if assignee:
            created_tasks = created_tasks.filter(assigned_to=assignee)
            flag = False
        if deadline:
            created_tasks = created_tasks.filter(deadline__date=deadline)
            flag = False
        if creation_date:
            created_tasks = created_tasks.filter(created_at__date=creation_date)
            flag = False
        if complete_reason:
            created_tasks = created_tasks.filter(completed_reason=complete_reason)
        if completed_at:
            created_tasks = created_tasks.filter(completed_at=completed_at)
            flag = False
        if flag:
            created_tasks_ = None
        else:
            created_tasks_ = created_tasks

        if total_tasks > 0:
            completed_percentage = ( completed_tasks / total_tasks) * 100
        else:
            completed_percentage = 0

            # Calculate percentage of created tasks
        if total_tasks > 0:
            created_percentage = (active_tasks / total_tasks) * 100
        else:
            created_percentage = 0
        COMPLETED_REASON_CHOICES = [
            None,
            'resolved_by_technician',
            'customer_not_available',
            'equipment_replaced',
            'service_completed',
            'task_canceled_by_client',
            'duplicate_request',
            'incorrect_information',
            'lack_of_resources',
            'external_factors',
            'task_closed_without_resolution',
            'transferred_to_another_team',
            'other', 'Other'
        ]
        context = {
            'created_tasks': active_tasks,
            'completed_tasks': completed_tasks,
            'total_tasks': total_tasks,
            'created_percentage': created_percentage,
            'completed_percentage': completed_percentage,
            "tickets": created_tasks_,
            "assignee_options": User.objects.filter(is_staff=True),
            "completed_reason": COMPLETED_REASON_CHOICES

        }

        return render(request, 'dashboard.html',
                      context)
    else:
        return redirect("/accounts/not-auth/")
