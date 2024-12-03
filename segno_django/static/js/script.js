function openTab(evt, tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    const currentTab = document.getElementById(tabName);
    currentTab.classList.add('active');

    const tabButtons = document.querySelectorAll('.tab');
    tabButtons.forEach(btn => btn.classList.remove('active'));
    evt.currentTarget.classList.add('active');
}

// Generate QR Code Function
function generateQRCode(formId, previewContainerId, previewImageId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);

    fetch("/generate-qr/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.qr_image) {
            const previewImage = document.getElementById(previewImageId);
            previewImage.src = data.qr_image;
            document.getElementById(previewContainerId).style.display = "block";
        } else {
            alert("Failed to generate QR code.");
        }
    })
    .catch(error => console.error("Error generating QR Code:", error));
}

// Export QR Code as PNG Function
function exportQRCodeAsPng(previewImageId) {
    const qrImage = document.getElementById(previewImageId).src;
    if (!qrImage) {
        alert("No QR code to export!");
        return;
    }

    const link = document.createElement("a");
    link.href = qrImage;
    link.download = "qrcode.png";
    link.click();
}

// Export Form Settings as JSON Function
function exportSettingsAsJson(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const settings = {};

    for (let [key, value] of formData.entries()) {
        settings[key] = value;
    }

    const blob = new Blob([JSON.stringify(settings, null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "settings.json";
    link.click();
}

// Import Settings from JSON File Function
function importSettingsFromJson(formId) {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = ".json";

    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function () {
            const settings = JSON.parse(reader.result);
            const form = document.getElementById(formId);

            for (const [key, value] of Object.entries(settings)) {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) input.value = value;
            }
        };

        reader.readAsText(file);
    });

    fileInput.click();
}