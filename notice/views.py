from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notice
from .forms import NoticeCreateForm, RegisterForm, StyledLoginForm
from django.core.exceptions import PermissionDenied

def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Чтобы оставить объявление, войдите на сайт')
            return redirect('login')
        
        form = NoticeCreateForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author_name = request.user
            notice.save()
            messages.success(request, 'Объявление создано')
            return redirect('notice:notice_list')
        else:
            messages.error(request, 'Исправьте ошибку в форме') 
    else:
        form = NoticeCreateForm()

    context = {
        'notices': notices,
        'form': form,
        'page_title': 'Доска объявлений'
    }
    return render(request, 'notice/notice_list.html', context)


def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    context = {
        'notice': notice,
        'page_title': notice.title
    }
    return render(request, 'notice/notice_details.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Аккаунт создан')
            return redirect('login')
        else:
            messages.error(request, 'Ошибки в форме')
    else:
        form = RegisterForm()

    context = {
        'form': form,
        'page_title': 'Регистрация'
    }

    return render(request, 'notice/register.html', context)

@login_required
def edit_notice(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)

    if not notice.can_edit(request.user):
        messages.error(request, 'Нет прав для редактирования')
        return redirect('notice:notice_details', notice_id=notice.id)

    if request.method == 'POST':
        form = NoticeCreateForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление отредактировано')
            return redirect('notice:notice_details', notice_id=notice.id)
        else:
            messages.error(request, 'Ошибки в форме')
    else:
        form = NoticeCreateForm(instance=notice)

    context = {
        'form': form,
        'notice': notice,
        'page_title': f'Редактирование {notice.title}'
    }
    return render(request, 'notice/notice_edit.html', context)

@login_required
def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)

    if not notice.can_delete(request.user):
        raise PermissionDenied('У вас нет прав на удаление')

    if request.method == 'POST':
        if 'confirm_delete' in request.POST:
            notice.delete()
            messages.success(request, 'Объявление удалено')
            return redirect('notice:notice_list')
        else:
            return redirect('notice:notice_details', notice_id=notice.id)

    context = {
        'notice': notice,
        'delete_confirm': True,
        'page_title': f'Удаление {notice.title}'
    }

    return render(request, 'notice/notice_details.html', context)

def login_view(request):
    if request.method == 'POST':
        form = StyledLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('notice:notice_list')
    else:
        form = StyledLoginForm()
    return render(request, 'notice/login.html', {'form': form})