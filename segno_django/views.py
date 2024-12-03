from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, FileResponse, JsonResponse
from django.conf import settings
import os
import segno
import segno.helpers
import json

def generate_qr(request: HttpRequest):
    if request.method == 'POST':
        # Example: Generate a generic QR code
        qr = segno.make("Example QR Code")
        qr_path = 'static/qr_codes/generated_qr.png'
        qr.save(qr_path, scale=10)
        return render(request, 'home.html', {'qr_image': qr_path})
    return HttpResponse("Invalid request method.", status=400)

def export_png():
    file_path = 'static/qr_codes/generated_qr.png'
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='image/png', as_attachment=True, filename='qr_code.png')
    return HttpResponse("QR code not found.", status=404)

def export_settings(request):
    if request.method == 'POST':
        settings = {"example_setting": "value"}  # Replace with actual settings
        response = JsonResponse(settings)
        response['Content-Disposition'] = 'attachment; filename="settings.json"'
        return response
    return HttpResponse("Invalid request method.", status=400)

def import_settings(request: HttpRequest):
    if request.method == 'POST' and request.FILES.get('settings_file'):
        file = request.FILES['settings_file']
        try:
            settings = json.load(file)
            # Apply settings as needed
            return HttpResponse("Settings imported successfully.")
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON file.", status=400)
    return HttpResponse("No file uploaded.", status=400)


def home(request: HttpRequest):
    if request.method == "POST":
        content = request.POST.get("content")
        # Generate Generic QR Code
        qr = segno.make(content)
        qr_code_path = "static/qr_codes/generic.png"
        qr.save(qr_code_path, scale=10)
        
        return render(request, "home.html", {"qr_code": qr_code_path})
    return render(request, "home.html")

def vcard(request: HttpRequest):
    qr_code_dir = os.path.join(settings.BASE_DIR, 'static', 'qr_codes')
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        organization = request.POST.get("organization", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        address = request.POST.get("address", "")
        url = request.POST.get("url", "")
        
        qr = segno.helpers.make_vcard(
            name=full_name,
            displayname=full_name,
            org=organization,
            email=email,
            phone=phone,
            street=address,
            url=url,
        )
        qr_code_path = "static/qr_codes/vcard.png"
        qr.save(qr_code_path, scale=10)
        return render(request, "vcard.html", {"qr_code": qr_code_path})
    return render(request, "vcard.html")

def mecard(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email", "")
        url = request.POST.get("url", "")
        
        qr = segno.helpers.make_mecard(
            name=full_name,
            phone=phone,
            email=email,
            url=url,
        )
        qr_code_path = "static/qr_codes/mecard.png"
        qr.save(qr_code_path, scale=10)
        return render(request, "mecard.html", {"qr_code": qr_code_path})
    return render(request, "mecard.html")

def email(request):
    if request.method == "POST":
        recipient = request.POST.get("recipient")
        subject = request.POST.get("subject", "")
        body = request.POST.get("body", "")
        
        # Generate Email QR Code
        qr = segno.helpers.make_email(to=recipient, subject=subject, body=body)
        qr_code_path = "static/qr_codes/email.png"
        qr.save(qr_code_path, scale=10)
        
        return render(request, "email.html", {"qr_code": qr_code_path})
    return render(request, "email.html")


def geo(request):
    if request.method == "POST":
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        altitude = request.POST.get("altitude", None)
        
        # Generate Geo QR Code
        qr = segno.helpers.make_geo(latitude=float(latitude), longitude=float(longitude), altitude=float(altitude) if altitude else None)
        qr_code_path = "static/qr_codes/geo.png"
        qr.save(qr_code_path, scale=10)
        
        return render(request, "geo.html", {"qr_code": qr_code_path})
    return render(request, "geo.html")


def wifi(request):
    if request.method == "POST":
        ssid = request.POST.get("ssid")
        password = request.POST.get("password")
        security = request.POST.get("security", "WPA")
        hidden = request.POST.get("hidden", "off") == "on"
        
        # Generate WiFi QR Code
        qr = segno.helpers.make_wifi(ssid=ssid, password=password, security=security, hidden=hidden)
        qr_code_path = "static/qr_codes/wifi.png"
        qr.save(qr_code_path, scale=10)
        
        return render(request, "wifi.html", {"qr_code": qr_code_path})
    return render(request, "wifi.html")


def epc(request):
    if request.method == "POST":
        name = request.POST.get("name")
        iban = request.POST.get("iban")
        amount = request.POST.get("amount")
        text = request.POST.get("text", "")
        
        # Generate EPC QR Code
        qr = segno.helpers.make_epc(name=name, iban=iban, amount=float(amount), text=text)
        qr_code_path = "static/qr_codes/epc.png"
        qr.save(qr_code_path, scale=10)
        
        return render(request, "epc.html", {"qr_code": qr_code_path})
    return render(request, "epc.html")
