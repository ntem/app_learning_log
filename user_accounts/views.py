from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def register(request):
    """User account registration"""

    if request.method == 'GET':
        # Reqest for registration form
        form = UserCreationForm
    elif request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()

            # log the user in and redirect
            login(request, new_user)
            return redirect('learning_logs:index')
    # return the registration form
    context = {'form': form}
    return render(request, 'registration/register.html', context)
