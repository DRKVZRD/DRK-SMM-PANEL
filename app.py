from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# ==========================================
# ⚙️ CONFIGURATION SETTINGS
# ==========================================
PROVIDER_API_URL = "https://peakerr.com/api/v2"
PROVIDER_API_KEY = "19cadb7c7ef863094d324b62ef1018a5"

# Peakerr Services tab se exact Service ID numbers yahan dalein:
PEAKERR_SERVICES = {
    "ig_followers": "100",  # Peakerr Instagram Followers Service ID
    "ig_likes": "101"       # Peakerr Instagram Likes Service ID
}

# WhatsApp Number (Country code 91 ke sath)
ADMIN_WHATSAPP_NUMBER = "919876543210" 
# ==========================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DRK HUB | Dark Booster</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: radial-gradient(circle at center, #1a0505 0%, #080202 100%); 
            color: #fce7e7; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            padding: 20px; 
            box-sizing: border-box; 
        }
        .container { 
            background: #110505; 
            border: 1px solid #7f1d1d; 
            padding: 30px; 
            border-radius: 14px; 
            width: 100%; 
            max-width: 440px; 
            box-shadow: 0 0 25px rgba(220, 38, 38, 0.25), inset 0 0 15px rgba(0,0,0,0.8); 
        }
        h1 { 
            text-align: center; 
            color: #ff2a2a; 
            margin: 0 0 4px 0; 
            letter-spacing: 3px; 
            text-transform: uppercase;
            text-shadow: 0 0 12px #dc2626, 0 0 24px #991b1b;
        }
        .tagline { 
            text-align: center; 
            font-size: 11px; 
            color: #991b1b; 
            margin-bottom: 22px; 
            letter-spacing: 1px;
            text-transform: uppercase;
            font-weight: bold;
        }
        label { 
            display: block; 
            margin-top: 14px; 
            font-size: 13px; 
            color: #f87171; 
            font-weight: 600; 
        }
        input, select { 
            width: 100%; 
            padding: 12px; 
            margin-top: 6px; 
            border-radius: 8px; 
            border: 1px solid #450a0a; 
            background: #080202; 
            color: #fff; 
            box-sizing: border-box; 
            font-size: 14px; 
            transition: all 0.2s ease;
        }
        input:focus, select:focus { 
            outline: none; 
            border-color: #dc2626; 
            box-shadow: 0 0 8px rgba(220, 38, 38, 0.5); 
        }
        .validation-msg {
            color: #ef4444;
            font-size: 12px;
            margin-top: 4px;
            display: none;
            font-weight: bold;
        }
        .price-card {
            background: #1f0808;
            border: 1px dashed #dc2626;
            border-radius: 8px;
            padding: 12px;
            margin-top: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .price-card span { font-size: 13px; color: #fca5a5; }
        .price-card b { font-size: 18px; color: #ef4444; text-shadow: 0 0 8px rgba(239, 68, 68, 0.6); }
        .btn-submit { 
            width: 100%; 
            padding: 14px; 
            margin-top: 22px; 
            background: linear-gradient(180deg, #dc2626 0%, #991b1b 100%); 
            color: #fff; 
            font-weight: bold; 
            border: 1px solid #ef4444; 
            border-radius: 8px; 
            font-size: 15px; 
            cursor: pointer; 
            letter-spacing: 1px;
            text-transform: uppercase;
            box-shadow: 0 0 15px rgba(220, 38, 38, 0.4);
            transition: 0.2s; 
        }
        .btn-submit:hover { 
            background: linear-gradient(180deg, #ef4444 0%, #b91c1c 100%); 
            box-shadow: 0 0 25px rgba(239, 68, 68, 0.7); 
        }
        #statusBox { 
            margin-top: 18px; 
            padding: 12px; 
            border-radius: 8px; 
            font-size: 13px; 
            display: none; 
            line-height: 1.5; 
        }
        .success { background: #064e3b; color: #6ee7b7; border: 1px solid #059669; display: block !important; }
        .error { background: #450a0a; color: #fca5a5; border: 1px solid #dc2626; display: block !important; }
        .manual-box { background: #1c0a0a; border: 1px solid #dc2626; color: #fca5a5; display: block !important; }
        .dm-btn { 
            display: inline-block; 
            width: 100%; 
            text-align: center; 
            box-sizing: border-box; 
            padding: 12px; 
            margin-top: 10px; 
            border-radius: 6px; 
            font-weight: bold; 
            text-decoration: none; 
            font-size: 14px; 
            background: #22c55e; 
            color: #000; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1> DRK HUB </h1>
        <div class="tagline">Underworld Boosting Engine</div>

        <form id="orderForm">
            <label for="service_type">Select Service:</label>
            <select id="service_type" onchange="handleServiceChange()" required>
                <optgroup label="📸 Instagram (Automated)">
                    <option value="ig_followers" data-rate="0.80">Instagram Followers (₹0.80 / Follower)</option>
                    <option value="ig_likes" data-rate="0.60">Instagram Likes (₹0.60 / Like)</option>
                </optgroup>
                <optgroup label="🔥 Free Fire (Manual DM)">
                    <option value="ff_likes" data-rate="0.60">Free Fire ID Profile Likes (₹0.60 / Like)</option>
                    <option value="craftland_subs" data-rate="0.80">Craftland Map Followers (₹0.80 / Sub)</option>
                </optgroup>
            </select>

            <label for="target_input" id="target_label">Target Instagram Profile / Link:</label>
            <input type="text" id="target_input" placeholder="https://instagram.com/your_username" oninput="validateLink()" required>
            <div id="linkError" class="validation-msg">⚠️ Invalid Link: Sahi Instagram profile URL ya valid ID dalein!</div>

            <label for="quantity">Quantity:</label>
            <input type="number" id="quantity" placeholder="e.g. 100" min="10" oninput="calculateTotal()" required>

            <div class="price-card">
                <span>Total Calculated Rate:</span>
                <b id="totalAmount">₹0.00</b>
            </div>

            <button type="submit" class="btn-submit" id="submitBtn">Proceed Order 🚀</button>
        </form>

        <div id="statusBox"></div>
    </div>

    <script>
        const waNumber = "{{ admin_wa }}";

        function calculateTotal() {
            const select = document.getElementById('service_type');
            const rate = parseFloat(select.options[select.selectedIndex].getAttribute('data-rate')) || 0;
            const qty = parseInt(document.getElementById('quantity').value) || 0;
            const total = (qty * rate).toFixed(2);
            document.getElementById('totalAmount').innerText = '₹' + total;
        }

        function validateLink() {
            const service = document.getElementById('service_type').value;
            const input = document.getElementById('target_input').value.trim();
            const errorBox = document.getElementById('linkError');

            if (!input) {
                errorBox.style.display = 'none';
                return true;
            }

            if (service.startsWith('ig_')) {
                const igUrlPattern = /^(https?:\\/\\/)?(www\\.)?instagram\\.com\\/[a-zA-Z0-9_.]+(\\/.*)?$/i;
                const igUsernamePattern = /^@?[a-zA-Z0-9_.]{1,30}$/;

                if (!igUrlPattern.test(input) && !igUsernamePattern.test(input)) {
                    errorBox.innerText = '⚠️ Invalid Link: Valid Instagram profile URL ya username dalein!';
                    errorBox.style.display = 'block';
                    return false;
                }
            } else {
                if (input.length < 5) {
                    errorBox.innerText = '⚠️ Invalid Format: Valid Free Fire UID ya Map Code dalein!';
                    errorBox.style.display = 'block';
                    return false;
                }
            }

            errorBox.style.display = 'none';
            return true;
        }

        function handleServiceChange() {
            const service = document.getElementById('service_type').value;
            const targetLabel = document.getElementById('target_label');
            const targetInput = document.getElementById('target_input');
            const submitBtn = document.getElementById('submitBtn');

            if (service.startsWith('ig_')) {
                targetLabel.innerText = 'Target Instagram Profile / Link:';
                targetInput.placeholder = 'https://instagram.com/your_username';
                submitBtn.innerText = 'Proceed Order 🚀';
            } else {
                targetLabel.innerText = 'Free Fire Player UID ya Map Code:';
                targetInput.placeholder = 'e.g. 1234567890 ya #FREEFIRE123';
                submitBtn.innerText = 'Order Via WhatsApp DM 💬';
            }

            validateLink();
            calculateTotal();
        }

        document.getElementById('orderForm').onsubmit = async (e) => {
            e.preventDefault();
            
            if (!validateLink()) {
                alert('Pehle sahi link ya username enter karein!');
                return;
            }

            const service = document.getElementById('service_type').value;
            const target = document.getElementById('target_input').value.trim();
            const qty = document.getElementById('quantity').value;
            const total = document.getElementById('totalAmount').innerText;
            const statusBox = document.getElementById('statusBox');

            statusBox.className = '';

            // Handle Manual Free Fire Orders via WhatsApp
            if (service === 'ff_likes' || service === 'craftland_subs') {
                const serviceName = service === 'ff_likes' ? 'Free Fire ID Likes' : 'Craftland Map Followers';
                const msg = encodeURIComponent(`💀 DRK HUB ORDER:\\n\\nService: ${serviceName}\\nUID/Code: ${target}\\nQuantity: ${qty}\\nTotal Rate: ${total}`);
                const waUrl = `https://wa.me/${waNumber}?text=${msg}`;

                statusBox.className = 'manual-box';
                statusBox.innerHTML = `
                    <b>💬 Free Fire Manual Confirmation:</b><br>
                    Total Amount: <b>${total}</b><br>
                    <a href="${waUrl}" target="_blank" class="dm-btn">Send Order on WhatsApp 📲</a>
                `;
                return;
            }

            // Handle Automated Instagram Orders
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
                    statusBox.innerHTML = `✅ <b>Order Placed!</b><br>Order ID: #${data.order}<br>Total Amount: ${total}`;
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
