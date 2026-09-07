from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, HouseholdCreateForm, HouseholdJoinForm
from .models import Household

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('onboarding')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def onboarding(request):
    # If user already has a household, redirect to dashboard
    if request.user.household:
        return redirect('dashboard')
        
    if request.method == 'POST':
        if 'create' in request.POST:
            create_form = HouseholdCreateForm(request.POST)
            join_form = HouseholdJoinForm()
            if create_form.is_valid():
                household = create_form.save()
                request.user.household = household
                request.user.role = 'admin'
                request.user.save()
                return redirect('dashboard')
        elif 'join' in request.POST:
            join_form = HouseholdJoinForm(request.POST)
            create_form = HouseholdCreateForm()
            if join_form.is_valid():
                code = join_form.cleaned_data['join_code']
                try:
                    household = Household.objects.get(join_code=code)
                    request.user.household = household
                    request.user.role = 'member'
                    request.user.save()
                    return redirect('dashboard')
                except Household.DoesNotExist:
                    join_form.add_error('join_code', 'Invalid join code.')
    else:
        create_form = HouseholdCreateForm()
        join_form = HouseholdJoinForm()

    return render(request, 'chores/onboarding.html', {
        'create_form': create_form,
        'join_form': join_form
    })

from datetime import date
from .models import Household, Task, SwapRequest, DutySchedule, CustomUser

@login_required
def dashboard(request):
    if not request.user.household:
        return redirect('onboarding')
        
    today = date.today()
    
    tasks = Task.objects.filter(
        duty_schedule__household=request.user.household,
        due_date=today
    )
    
    todo_tasks = tasks.filter(status=False).order_by('deadline_time')
    done_tasks = tasks.filter(status=True).order_by('deadline_time')
    
    if request.method == 'POST' and 'toggle_task' in request.POST:
        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(id=task_id, duty_schedule__household=request.user.household)
            task.status = not task.status
            task.save()
            return redirect('dashboard')
        except Task.DoesNotExist:
            pass
            
    return render(request, 'chores/dashboard.html', {
        'todo_tasks': todo_tasks,
        'done_tasks': done_tasks,
        'today': today
    })

@login_required
def swaps(request):
    if not request.user.household:
        return redirect('onboarding')

    household = request.user.household
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Handle Swap Request Accept/Reject
        if action in ['accept', 'reject']:
            swap_id = request.POST.get('swap_id')
            try:
                swap = SwapRequest.objects.get(id=swap_id, to_user=request.user, status='pending')
                if action == 'accept':
                    swap.status = 'accepted'
                    # Perform the swap: assign the target_schedule to the to_user
                    schedule = swap.target_schedule
                    schedule.assigned_user = request.user
                    schedule.save()
                else:
                    swap.status = 'rejected'
                swap.save()
            except SwapRequest.DoesNotExist:
                pass
                
        # Handle new swap request
        elif action == 'request_swap':
            target_schedule_id = request.POST.get('schedule_id')
            to_user_id = request.POST.get('to_user_id')
            try:
                schedule = DutySchedule.objects.get(id=target_schedule_id, assigned_user=request.user)
                to_user = CustomUser.objects.get(id=to_user_id, household=household)
                SwapRequest.objects.create(
                    from_user=request.user,
                    to_user=to_user,
                    target_schedule=schedule,
                    status='pending'
                )
            except (DutySchedule.DoesNotExist, CustomUser.DoesNotExist, ValueError):
                pass
                
        return redirect('swaps')

    # Get user's upcoming schedules
    my_schedules = DutySchedule.objects.filter(assigned_user=request.user, week_start_date__gte=date.today())
    
    # Get other members to send requests to
    other_members = CustomUser.objects.filter(household=household).exclude(id=request.user.id)
    
    # Get pending swap requests TO the user
    incoming_requests = SwapRequest.objects.filter(to_user=request.user, status='pending')
    
    # Get swap requests FROM the user
    outgoing_requests = SwapRequest.objects.filter(from_user=request.user).order_by('-created_at')

    return render(request, 'chores/swaps.html', {
        'my_schedules': my_schedules,
        'other_members': other_members,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests
    })

from django.db import IntegrityError

@login_required
def manage_chores(request):
    if not request.user.household:
        return redirect('onboarding')

    household = request.user.household

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create_schedule':
            week_start_date = request.POST.get('week_start_date')
            assigned_user_id = request.POST.get('assigned_user_id')
            try:
                assigned_user = CustomUser.objects.get(id=assigned_user_id, household=household)
                DutySchedule.objects.create(
                    week_start_date=week_start_date,
                    assigned_user=assigned_user,
                    household=household
                )
            except (CustomUser.DoesNotExist, IntegrityError, ValueError):
                pass
                
        elif action == 'create_task':
            schedule_id = request.POST.get('schedule_id')
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            due_date = request.POST.get('due_date')
            deadline_time = request.POST.get('deadline_time')
            
            try:
                schedule = DutySchedule.objects.get(id=schedule_id, household=household)
                Task.objects.create(
                    title=title,
                    description=description,
                    due_date=due_date,
                    deadline_time=deadline_time,
                    duty_schedule=schedule
                )
            except (DutySchedule.DoesNotExist, ValueError):
                pass
                
        return redirect('manage_chores')

    members = CustomUser.objects.filter(household=household)
    schedules = DutySchedule.objects.filter(household=household, week_start_date__gte=date.today()).order_by('week_start_date')
    
    return render(request, 'chores/manage.html', {
        'members': members,
        'schedules': schedules,
    })
