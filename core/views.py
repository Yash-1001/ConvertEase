import os
import uuid
import requests
import json
import time
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
from .utils.adobe_auth import get_adobe_access_token
@never_cache
@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'core/dashboard.html')

@never_cache
@login_required(login_url='login')
def pdf_to_excel_view(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        unique_id = uuid.uuid4().hex
        upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
        converted_path = os.path.join(settings.MEDIA_ROOT, 'converted')
        os.makedirs(upload_path, exist_ok=True)
        os.makedirs(converted_path, exist_ok=True)

        pdf_filepath = os.path.join(upload_path, f"{unique_id}.pdf")
        excel_filepath = os.path.join(converted_path, f"{unique_id}.xlsx")

        # Save uploaded PDF
        with open(pdf_filepath, 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        try:
            access_token, client_id = get_adobe_access_token(return_client_id=True)

            # 1. Create asset (upload slot)
            assets_url = "https://pdf-services.adobe.io/assets"
            assets_headers = {
                "Authorization": f"Bearer {access_token}",
                "x-api-key": client_id,
                "Content-Type": "application/json"
            }
            assets_data = {
                "mediaType": "application/pdf"
            }
            assets_resp = requests.post(assets_url, headers=assets_headers, json=assets_data)
            assets_resp.raise_for_status()
            assets_info = assets_resp.json()
            upload_url = assets_info["uploadUri"]
            asset_id = assets_info["assetID"]

            # 2. Upload the PDF to the upload URL
            with open(pdf_filepath, "rb") as f:
                upload_resp = requests.put(upload_url, data=f, headers={"Content-Type": "application/pdf"})
                print("Upload status:", upload_resp.status_code)
                print("Upload response:", upload_resp.text)
                upload_resp.raise_for_status()
                time.sleep(2)

            # 3. Create export job using assetID
            job_url = "https://pdf-services.adobe.io/operation/exportpdf"
            job_headers = {
                "Authorization": f"Bearer {access_token}",
                "x-api-key": client_id,
                "Content-Type": "application/json"
            }
            job_data = {
                "input": {
                    "assetID": asset_id,
                },
                "exportFormat": "xlsx"
            }
            print("Access token:", access_token)
            print("Client ID:", client_id)
            print("Asset ID:", asset_id)
            print("Job headers:", job_headers)
            print("Job data:", job_data)
            job_response = requests.post(job_url, headers=job_headers, json=job_data)
            job_response.raise_for_status()
            job_info = job_response.json()

            # 4. Poll for job completion
            status_url = job_info["statusUri"]
            while True:
                status_resp = requests.get(status_url, headers=job_headers)
                status_resp.raise_for_status()
                status_json = status_resp.json()
                status = status_json.get("status")
                if status == "done":
                    break
                elif status == "failed":
                    return render(request, "core/pdf_to_excel.html", {"error": "Adobe conversion failed."})
                time.sleep(2)

            # 5. Download the result
            result_url = status_json["output"]["uri"]
            result_resp = requests.get(result_url)
            with open(excel_filepath, "wb") as out:
                out.write(result_resp.content)

            return FileResponse(open(excel_filepath, 'rb'), as_attachment=True, filename=f"{unique_id}.xlsx")

        except Exception as e:
            return render(request, "core/pdf_to_excel.html", {"error": f"Error: {str(e)}"})

    return render(request, "core/pdf_to_excel.html")


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
