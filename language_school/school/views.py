from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Course, Teacher, Enrollment, CourseMaterial
from django.contrib.auth import logout
from .forms import UserEditForm

def home(request):
    return render(request, 'school/home.html')


def course_list(request):
    courses = Course.objects.filter(is_active=True)
    return render(request, 'school/course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk, is_active=True)
    return render(request, 'school/course_detail.html', {'course': course})


def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'school/teacher_list.html', {'teachers': teachers})


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id, is_active=True)

    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, 'Вы уже подали заявку на этот курс')
        return redirect('course_detail', pk=course_id)

    Enrollment.objects.create(student=request.user, course=course)
    messages.success(request, 'Заявка успешно подана! Ожидайте подтверждения.')
    return redirect('profile')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'school/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)

    enrollments = Enrollment.objects.filter(student=request.user)
    approved_courses = enrollments.filter(status='approved')
    pending_enrollments = enrollments.filter(status='pending')
    rejected_enrollments = enrollments.filter(status='rejected')

    course_materials = {}
    for enrollment in approved_courses:
        materials = CourseMaterial.objects.filter(course=enrollment.course)
        course_materials[enrollment.course.id] = materials

    context = {
        'form': form,
        'enrollments': enrollments,
        'approved_courses': approved_courses,
        'pending_enrollments': pending_enrollments,
        'rejected_enrollments': rejected_enrollments,
        'course_materials': course_materials,
    }
    return render(request, 'school/profile.html', context)

def custom_logout(request):
    logout(request)
    return redirect('home')