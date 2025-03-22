from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from booking.forms import CustomUserCreationForm
from .models import FitnessClass, Booking

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("fitness-classes/") 
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, "booking/login.html")

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful!")
            return redirect("login")  # Redirect to login after successful registration
        else:
            messages.error(request, "Registration failed. Please check your inputs.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, "booking/register.html", {"form": form})

@login_required
def fitness_list(request):
    classes = FitnessClass.objects.all()
    return render(request, "booking/fitness_Classes.html", {"classes": classes})


@login_required
def join_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    if Booking.objects.filter(user=request.user, fitness_class=fitness_class).exists():
        messages.warning(request, "You have already joined this class.")
    else:
        Booking.objects.create(user=request.user, fitness_class=fitness_class)
        messages.success(request, "You successfully joined the class!")
              # Send email notification
        subject = "Class Booking Confirmation"
        message = f"Hi {request.user.username},\n\nYou have successfully joined the class: {fitness_class.name}.\n\nDetails:\nInstructor: {fitness_class.instructor.username}\nSchedule: {fitness_class.schedule}\n\nThank you for booking with us!"
        recipient_list = [request.user.email]
        send_mail(subject, message,'c.umuhire@alustudent.com', recipient_list)

    return redirect("class_list")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")  # Redirect to the login page after logout