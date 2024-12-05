from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
import os
import segno
import segno.helpers
import base64
import io

def home(request: HttpRequest):
    qr_image = None
    if request.method == 'POST':
        try:
            # Get form data
            content = request.POST.get('content')
            scale = int(request.POST.get('scale'))
            border = int(request.POST.get('border'))
            error_correction = request.POST.get('error-correction')
            
            # Color settings
            dark = request.POST.get('dark')
            light = request.POST.get('light')
            data_dark = request.POST.get('data-dark')
            data_light = request.POST.get('data-light')

            # Map error correction
            error_levels = {
                'L': 1,  # 7% recovery
                'M': 0,  # 15% recovery
                'Q': 3,  # 25% recovery
                'H': 2   # 30% recovery
            }

            # Generate QR code
            qr = segno.make_qr(
                content, 
                error=error_levels.get(error_correction)
            )

            # Save to buffer with color customization
            buffer = io.BytesIO()
            qr.save(
                buffer, 
                kind='png', 
                scale=scale, 
                border=border,
                dark=dark,
                light=light,
                data_dark=data_dark,
                data_light=data_light
            )
            
            # Convert to base64
            qr_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        except Exception as e:
            print(f"QR Code Generation Error: {e}")

    return render(request, 'home.html', {'qr_image': qr_image})

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