from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# ==========================================
# ⚙️ CONFIGURATION SETTINGS
# ==========================================
# 1. Automated Instagram Provider (Peakerr)
PROVIDER_API_URL = "https://peakerr.com/api/v2"
PROVIDER_API_KEY = "19cadb7c7ef863094d324b62ef1018a5"

# Peakerr Services tab se Instagram ke exact Service ID numbers yahan dalein:
PEAKERR_SERVICES = {
    "ig_followers": "100",  # Example: Peakerr Instagram Followers Service ID
    "ig_likes": "101"       # Example: Peakerr Instagram Likes Service ID
}

# 2. Manual Free Fire DM Details (Aapka WhatsApp / Instagram)
# WhatsApp number (Country code 91 ke sath, bina + ke, e.g. "919876543210")
ADMIN_WHATSAPP_NUMBER = "919876543210" 
ADMIN_IG_USERNAME = "your_instagram_handle" 
# ==========================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nexus SMM & Gaming Hub</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b0f19; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; box-sizing: border-box; }
        .container { background: #131b2e; border: 1px solid #1e293b; padding: 30px; border-radius: 12px; width: 100%; max-width: 440px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        h2 { text-align: center; color: #f59e0b; margin-top: 0; letter-spacing: 0.5px; }
        .tagline { text-align: center; font-size: 12px; color: #64748b; margin-top: -12px; margin-bottom: 20px; }
        label { display: block; margin-top: 14px; font-size: 13px; color: #94a3b8; font-weight: bold; }
        input, select { width: 100%; padding: 12px; margin-top: 6px; border-radius: 8px; border: 1px solid #334155; background: #0b0f19; color: #fff; box-sizing: border-box; font-size: 14px; }
        input:focus, select:focus { outline: 1px solid #f59e0b; border-color: #f59e0b; }
        .btn-submit { width: 100%; padding: 14px; margin-top: 22px; background: #f59e0b; color: #000; font-weight: bold; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; transition: 0.2s; }
        .btn-submit:hover { background: #d97706; }
        #statusBox { margin-top: 20px; padding: 12px; border-radius: 8px; font-size: 13px; display: none; line-height: 1.5; }
        .success { background: #064e3b; color: #6ee7b7; border: 1px solid #059669; display: block !important; }
        .error { background: #7f1d1d; color: #fca5a5; border: 1px solid #dc2626; display: block !important; }
        .manual-box { background: #1e293b; border: 1px solid #3b82f6; color: #93c5fd; display: block !important; }
        .dm-btn { display: inline-block; width: 100%; text-align: center; box-sizing: border-box; padding: 12px; margin-top: 10px; border-radius: 6px; font-weight: bold; text-decoration: none; font-size: 14px; cursor: pointer; }
        .wa-btn { background: #22c55e; color: #000; }
    </style>
</head>
<body>
    <div class="container">
        <h2>⚡ Nexus Booster Hub</h2>
        <div class="tagline">Auto Instagram API + Manual FF Gaming Booster</div>

        <form id="orderForm">
            <label for="service_type">Service Select Karo:</label>
            <select id="service_type" onchange="updatePlaceholder()" required>
                <optgroup label="📸 Instagram (Instant API Auto)">
                    <option value="ig_followers">Instagram Followers 🚀</option>
                    <option value="ig_likes">Instagram Likes ❤️</option>
                </optgroup>
                <optgroup label="🔥 Free Fire (Manual DM Order)">
                    <option value="ff_likes">Free Fire ID Profile Likes 👍</option>
                    <option value="craftland_subs">Craftland Map Followers / Stars ⭐</option>
                </optgroup>
            </select>

            <label for="target_input" id="target_label">Profile Link / Username:</label>
            <input type="text" id="target_input" placeholder="https://instagram.com/username" required>

            <label for="quantity">Quantity:</label>
            <input type="number" id="quantity" placeholder="e.g. 100" min="10" required>

            <button type="submit" class="btn-submit" id="submitBtn">Proceed Order 🚀</button>
        </form>

        <div id="statusBox"></div>
    </div>

    <script>
        const waNumber = "{{ admin_wa }}";

        function updatePlaceholder() {
            const service = document.getElementById('service_type').value;
            const targetLabel = document.getElementById('target_label');
            const targetInput = document.getElementById('target_input');
            const submitBtn = document.getElementById('submitBtn');

            if (service.startsWith('ig_')) {
                targetLabel.innerText = 'Instagram Profile Link / Post URL:';
                targetInput.placeholder = 'https://instagram.com/username';
                submitBtn.innerText = 'Submit Auto Order 🚀';
            } else {
                targetLabel.innerText = 'Free Fire Player UID ya Map Code:';
                targetInput.placeholder = 'e.g. 1234567890 ya #FREEFIRE123';
                submitBtn.innerText = 'Order Via WhatsApp DM 💬';
            }
        }

        document.getElementById('orderForm').onsubmit = async (e) => {
            e.preventDefault();
            const service = document.getElementById('service_type').value;
            const target = document.getElementById('target_input').value;
            const qty = document.getElementById('quantity').value;
            const statusBox = document.getElementById('statusBox');

            statusBox.className = '';

            // Handle Manual Free Fire Orders via WhatsApp Direct Link
            if (service === 'ff_likes' || service === 'craftland_subs') {
                const serviceName = service === 'ff_likes' ? 'Free Fire ID Likes' : 'Craftland Map Followers';
                const msg = encodeURIComponent(`Hi, I want to order:\\n\\nService: ${serviceName}\\nUID/Code: ${target}\\nQuantity: ${qty}`);
                const waUrl = `https://wa.me/${waNumber}?text=${msg}`;

                statusBox.className = 'manual-box';
                statusBox.innerHTML = `
                    <b>💬 Free Fire Manual Processing:</b><br>
                    Free Fire orders direct DM ke zariye confirm hote hain.<br>
                    <a href="${waUrl}" target="_blank" class="dm-btn wa-btn">Open WhatsApp & Send Order 📲</a>
                `;
                return;
            }

            // Handle Automated Instagram Orders via Backend API
            statusBox.innerText = 'Order process ho raha hai...';
            statusBox.style.display = 'block';

            try {
                const res = await fetch('/api/order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ service_type: service, target_id: target, quantity: qty })
                });
                const data = await res.json();

                if (data.order) {
                    statusBox.className = 'success';
                    statusBox.innerHTML = `✅ <b>Order Placed!</b><br>Order ID: #${data.order}<br>Delivery Start Ho Rahi Hai.`;
                } else {
                    statusBox.className = 'error';
                    statusBox.innerHTML = `❌ <b>Failed:</b> ${data.error || JSON.stringify(data)}`;
                }
            } catch (err) {
                statusBox.className = 'error';
                statusBox.innerText = 'Network error ya server issue!';
            }
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, admin_wa=ADMIN_WHATSAPP_NUMBER)

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    service_type = data.get('service_type')
    target_id = data.get('target_id')
    quantity = data.get('quantity')

    service_id = PEAKERR_SERVICES.get(service_type)
    if not service_id:
        return jsonify({'error': 'Invalid Auto Service'}), 400

    payload = {
        'key': PROVIDER_API_KEY,
        'action': 'add',
        'service': service_id,
        'link': target_id,
        'quantity': quantity
    }

    try:
        response = requests.post(PROVIDER_API_URL, data=payload, timeout=15)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
