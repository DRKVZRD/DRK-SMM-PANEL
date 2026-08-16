from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# ==========================================
# ⚙️ APNI REAL PROVIDER DETAILS YAHAN DALEIN
# ==========================================
PROVIDER_API_URL = "https://example-smm-provider.com/api/v2"  # Provider ka API URL
PROVIDER_API_KEY = "PASTE_YOUR_API_KEY_HERE"                 # Provider se mili Secret Key

SERVICE_IDS = {
    "ff_likes": "101",        # Free Fire Likes ka Service ID number
    "craftland_subs": "102"    # Craftland Followers/Stars ka Service ID number
}
# ==========================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Fire Booster Hub</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b0f19; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: #131b2e; border: 1px solid #1e293b; padding: 30px; border-radius: 12px; width: 100%; max-width: 440px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }
        h2 { text-align: center; color: #f59e0b; margin-top: 0; }
        label { display: block; margin-top: 15px; font-size: 13px; color: #94a3b8; font-weight: bold; }
        input, select { width: 100%; padding: 12px; margin-top: 6px; border-radius: 8px; border: 1px solid #334155; background: #0b0f19; color: #fff; box-sizing: border-box; font-size: 14px; }
        button { width: 100%; padding: 14px; margin-top: 24px; background: #f59e0b; color: #000; font-weight: bold; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; }
        button:hover { background: #d97706; }
        #statusBox { margin-top: 20px; padding: 12px; border-radius: 8px; font-size: 13px; display: none; line-height: 1.5; }
        .success { background: #064e3b; color: #6ee7b7; border: 1px solid #059669; display: block !important; }
        .error { background: #7f1d1d; color: #fca5a5; border: 1px solid #dc2626; display: block !important; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔥 Free Fire Booster Hub</h2>
        <form id="orderForm">
            <label for="service_type">Service Select Karo:</label>
            <select id="service_type" required>
                <option value="ff_likes">Free Fire ID Profile Likes 👍</option>
                <option value="craftland_subs">Craftland Map Followers / Stars ⭐</option>
            </select>

            <label for="target_id">Player UID ya Map Code:</label>
            <input type="text" id="target_id" placeholder="e.g. 1234567890 ya #FREEFIRE123" required>

            <label for="quantity">Quantity:</label>
            <input type="number" id="quantity" placeholder="e.g. 100" min="10" required>

            <button type="submit">Submit Order 🚀</button>
        </form>
        <div id="statusBox"></div>
    </div>

    <script>
        document.getElementById('orderForm').onsubmit = async (e) => {
            e.preventDefault();
            const statusBox = document.getElementById('statusBox');
            statusBox.className = '';
            statusBox.innerText = 'Order process ho raha hai...';
            statusBox.style.display = 'block';

            const payload = {
                service_type: document.getElementById('service_type').value,
                target_id: document.getElementById('target_id').value,
                quantity: document.getElementById('quantity').value
            };

            try {
                const res = await fetch('/api/order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const data = await res.json();

                if (data.order) {
                    statusBox.className = 'success';
                    statusBox.innerHTML = `✅ <b>Order Confirmed!</b><br>Order ID: ${data.order}<br>UID: ${payload.target_id}`;
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
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    service_type = data.get('service_type')
    target_id = data.get('target_id')
    quantity = data.get('quantity')

    service_id = SERVICE_IDS.get(service_type)

    if not service_id:
        return jsonify({'error': 'Invalid Service Selected'}), 400

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
