with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add email alerts form in profile page before TikTok Connect
old_connect = '<h3>Connect TikTok Profile</h3>'
new_email = '''<h3>Email Alerts</h3>
                <p style="font-size:0.9rem;color:#666;">Get notified when high‑opportunity trends appear.</p>
                <input type="email" id="alert-email" placeholder="Your email" class="form-control">
                <button type="button" class="btn btn-primary" onclick="subscribeAlerts()">Subscribe</button>
                <div id="alert-status" style="margin-top:0.5rem;font-size:0.85rem;"></div>
                <hr style="margin:1.5rem 0;">
                <h3>Connect TikTok Profile</h3>'''
content = content.replace(old_connect, new_email)

# Add subscribeAlerts function before connectTikTok
old_connect_func = 'function connectTikTok() {'
new_alert_func = '''function subscribeAlerts() {
            var email = document.getElementById("alert-email").value;
            if (!email) { showToast("Enter your email", "error"); return; }
            fetch(API_URL + "/alerts/subscribe", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({email: email})
            })
            .then(function(r){ return r.json(); })
            .then(function(d){
                document.getElementById("alert-status").innerHTML = "✅ " + d.message;
                showToast(d.message, "success");
            })
            .catch(function(){ showToast("Subscription failed", "error"); });
        }
        
        function connectTikTok() {'''
content = content.replace(old_connect_func, new_alert_func)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Email alert UI added")
