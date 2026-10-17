
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, TeacherForm, StudentForm
from .models import Teacher, Student, User

# ----------------- Authentication ----------------- #

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.role == 'ADMIN':
        teachers = Teacher.objects.all()
        students = Student.objects.all() # Admin views all students (Read-only)[cite: 1, 2]
        return render(request, 'admin_dashboard.html', {'teachers': teachers, 'students': students})
    else:
        teacher_profile = getattr(request.user, 'teacher_profile', None)
        students = Student.objects.filter(teacher=teacher_profile) if teacher_profile else []
        return render(request, 'teacher_dashboard.html', {'students': students})

# ----------------- Admin: Teacher CRUD ----------------- #

@login_required
def teacher_create(request):
    if request.user.role != 'ADMIN':
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'TEACHER'
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            return redirect('dashboard')
    else:
        user_form = CustomUserCreationForm()
        teacher_form = TeacherForm()
    return render(request, 'teacher_form.html', {'user_form': user_form, 'teacher_form': teacher_form})

@login_required
def teacher_delete(request, pk):
    if request.user.role == 'ADMIN':
        teacher = get_object_or_404(Teacher, pk=pk)
        teacher.user.delete() # Deletes user and associated teacher
    return redirect('dashboard')

# ----------------- Teacher: Student CRUD ----------------- #

@login_required
def student_create(request):
    if request.user.role != 'TEACHER':
        return redirect('dashboard')
    
    teacher_profile = get_object_or_404(Teacher, user=request.user)
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.teacher = teacher_profile # Automatically assign logged-in teacher
            student.save()
            return redirect('dashboard')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_update(request, pk):
    teacher_profile = get_object_or_404(Teacher, user=request.user)
    student = get_object_or_404(Student, pk=pk, teacher=teacher_profile)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_delete(request, pk):
    teacher_profile = get_object_or_404(Teacher, user=request.user)
    student = get_object_or_404(Student, pk=pk, teacher=teacher_profile)
    student.delete()
    return redirect('dashboard')