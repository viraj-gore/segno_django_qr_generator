from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.conf import settings
import os
import segno
import segno.helpers
import base64
import io

def home(request):
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

            return render(request, 'home.html', {'qr_image': qr_image})

        except Exception as e:
            print(f"QR Code Generation Error: {e}")

    return render(request, 'home.html')

def vcard(request: HttpRequest):
    v_code=None
    if request.method == "POST":
        try:
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

            buffer = io.BytesIO()

            qr.save(
                    buffer, 
                    kind='png', 
                    scale='5', 
                )
            # Convert to base64
            v_code = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return render(request, "vcard.html", {"qr_code": v_code})
        
        except Exception as e:
            print(f"QR Code Generation Error: {e}")
    return render(request, "vcard.html")



def mecard(request):
    me_code = None
    if request.method == "POST":
        try:
            name = request.POST.get('full_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            url = request.POST.get('url')
            
            qr = segno.helpers.make_mecard(
                name=name,
                phone=phone,
                email=email,
                url=url,
            )

            buffer = io.BytesIO()

            qr.save(
                    buffer, 
                    kind='png', 
                    scale='5', 
                )
            # Convert to base64
            me_code = base64.b64encode(buffer.getvalue()).decode('utf-8')

            return render(request, "mecard.html", {'qr_code': me_code})
        
        except Exception as e:
            print(f"QR Code Generation Error: {e}")
    return render(request, "mecard.html")

def email(request):
    email_code = None
    if request.method == "POST":
        try:
            recipient = request.POST.get("recipient")
            subject = request.POST.get("subject", "")
            body = request.POST.get("body", "")
            
            # Generate Email QR Code
            qr = segno.helpers.make_email(to=recipient, subject=subject, body=body)

            buffer = io.BytesIO()

            qr.save(
                    buffer, 
                    kind='png', 
                    scale='5', 
                )
            # Convert to base64
            email_code = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return render(request, "email.html", {"qr_code": email_code})
        
        except Exception as e:
            print(f"QR Code Generation Error: {e}")

    return render(request, "email.html")


def geo(request):
    """
    View to generate a Geo QR Code based on latitude and longitude
    """
    geo_code = None

    if request.method == 'POST':
        # Get latitude and longitude from form submission
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        try:
            # Validate latitude and longitude
            lat = float(latitude)
            lon = float(longitude)

            # Create geo URI for QR Code
            geo_uri = f"geo:{lat},{lon}"

            # Generate QR Code with Segno
            qr = segno.make(geo_uri)

            # Save QR Code to a bytes buffer
            buffer = io.BytesIO()
            qr.save(buffer, kind='png', scale=5)
            
            # Encode the QR Code to base64 for HTML display
            
            geo_code = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return render(request, "geo.html", {"qr_code": geo_code})
        
        except Exception as e:
            print(f"QR Code Generation Error: {e}")

    return render(request, "geo.html")


def wifi(request):
    wifi_code = None
    if request.method == "POST":
        try:
            ssid = request.POST.get("ssid")
            password = request.POST.get("password")
            security = request.POST.get("security", "WPA")
            hidden = request.POST.get("hidden", "off") == "on"
            
            # Generate WiFi QR Code
            qr = segno.helpers.make_wifi(ssid=ssid, password=password, security=security, hidden=hidden)

            buffer = io.BytesIO()

            qr.save(
                    buffer, 
                    kind='png', 
                    scale='5', 
                )
            
            # Convert to base64
            wifi_code = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return render(request, "wifi.html", {"qr_code": wifi_code})
        
        except Exception as e:
            print(f"QR Code Generation Error: {e}")
        
    return render(request, "wifi.html")


def epc(request):
    epc_code= None
    if request.method == "POST":
        try:
            bic = request.POST.get("bic")
            iban = request.POST.get("iban")
            amount = request.POST.get("amount")
            name = request.POST.get("name")
            
            # Generate EPC QR Code
            qr = segno.helpers.make_epc_qr(name=name, iban=iban, amount=float(amount), bic=bic)

            epc_string = "\n".join([
                "BCD",      # Service Tag
                "002",      # Version
                "1",        # Encoding (UTF-8)
                "SCT",      # Identification
                bic or "",  # BIC (optional)
                name,       # Account Holder Name
                iban,       # IBAN
                f"EUR{float(amount) if amount else ''}",  # Amount with EUR prefix
                "",         # Purpose (optional)
                "",         # Remittance Reference (optional)
                ""          # Unstructured Information (optional)
            ])
            qr = segno.make(epc_string)
            
            buffer = io.BytesIO()

            qr.save(
                    buffer, 
                    kind='png', 
                    scale='5', 
                )
            
            # Convert to base64
            epc_code = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return render(request, "epc.html", {"qr_code": epc_code})
        
        except Exception as e:
            print(f"QR Code Generation Error: {e}")
        
        
    return render(request, "epc.html")