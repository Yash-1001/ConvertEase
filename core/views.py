import os
import uuid
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseNotAllowed
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from core.converters.json_to_excel import convert_json_to_excel

@never_cache
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'core/dashboard.html')




@never_cache
@login_required(login_url='login')
def json_to_excel_view(request):
    if request.method == 'POST':
        json_file = request.FILES.get('json_file')

        if not json_file:
            return render(request, 'core/convert.html', {'error': 'No file uploaded.'})

        unique_id = uuid.uuid4().hex
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        converted_path = os.path.join(settings.MEDIA_ROOT, 'converted')

        os.makedirs(upload_path, exist_ok=True)
        os.makedirs(converted_path, exist_ok=True)

        json_filepath = os.path.join(upload_path, f"{unique_id}.json")
        excel_filepath = os.path.join(converted_path, f"{unique_id}.xlsx")

        with open(json_filepath, 'wb+') as destination:
            for chunk in json_file.chunks():
                destination.write(chunk)

        try:
            with open(json_filepath, 'r') as f:
                convert_json_to_excel(f, excel_filepath)
        except Exception as e:
            return render(request, 'core/convert.html', {'error': f'Error processing file: {e}'})

        try:
            response = FileResponse(open(excel_filepath, 'rb'), as_attachment=True, filename=f"{unique_id}.xlsx")
            return response
        except Exception as e:
            return render(request, 'core/convert.html', {'error': f'Error sending file: {e}'})

    return render(request, 'core/convert.html')


@csrf_protect
@never_cache
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if not username or not password or not confirm:
            return render(request, 'core/register.html', {'error': 'All fields are required.'})
        if password != confirm:
            return render(request, 'core/register.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {'error': 'Username already exists.'})

        User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'core/register.html')


@csrf_protect
@never_cache
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/login.html')


@csrf_protect
@never_cache
def logout_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    logout(request)
    response = redirect('login')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response
