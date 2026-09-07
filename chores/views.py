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

@login_required
def dashboard(request):
    if not request.user.household:
        return redirect('onboarding')
    return render(request, 'chores/dashboard.html')
