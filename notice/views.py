from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Notice
from .forms import NoticeCreateForm

def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = NoticeCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление создано')
            return redirect('notice:notice_list')
        else:
            messages.error(request, 'Исправьте ошибку в форме')
            context = {
                'notices': notices,
                'form': form,
                'page_title': 'Доска объявлений'
            }
            return render(request, 'notice/notice_list.html', context)  
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