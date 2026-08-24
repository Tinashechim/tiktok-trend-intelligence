with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Premium section in profile page after auth section
old_connect = '<h3>Connect TikTok Profile</h3>'
new_premium = '''<hr style="margin:1.5rem 0;">
                <h3>💎 Premium</h3>
                <p style="font-size:0.9rem;color:#666;">Unlock advanced analytics, unlimited saved trends, and priority alerts.</p>
                <div id="premium-section">
                    <p>Status: <strong id="premium-status">Free</strong></p>
                    <button class="btn btn-primary" onclick="upgradePremium()">Upgrade to Premium</button>
                    <div id="premium-message" style="margin-top:0.5rem;font-size:0.85rem;"></div>
                </div>
                <hr style="margin:1.5rem 0;">
                <h3>Connect TikTok Profile</h3>'''
content = content.replace(old_connect, new_premium)

# Add premium functions before connectTikTok
old_connect_func = 'function connectTikTok() {'
new_premium_func = '''function upgradePremium() {
            var authUser = localStorage.getItem("authUser");
            if (!authUser) { showToast("Please login first", "error"); return; }
            var user = JSON.parse(authUser);
            fetch(API_URL + "/premium/upgrade", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({user_id: user.id, promo_code: ""})
            })
            .then(function(r){ return r.json(); })
            .then(function(d){
                document.getElementById("premium-status").textContent = "Premium ✅";
                document.getElementById("premium-message").innerHTML = "🎉 " + d.message;
                showToast(d.message, "success");
            })
            .catch(function(){ showToast("Upgrade failed", "error"); });
        }
        
        function checkPremium() {
            var authUser = localStorage.getItem("authUser");
            if (authUser) {
                var user = JSON.parse(authUser);
                fetch(API_URL + "/premium/status/" + user.id)
                    .then(function(r){ return r.json(); })
                    .then(function(d){
                        if (d.is_premium) {
                            document.getElementById("premium-status").textContent = "Premium ✅";
                        } else {
                            document.getElementById("premium-status").textContent = "Free";
                        }
                    })
                    .catch(function(){});
            }
        }
        
        function connectTikTok() {'''
content = content.replace(old_connect_func, new_premium_func)

# Call checkPremium after checkAuth
content = content.replace('checkAuth();', 'checkAuth();\n        checkPremium();')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Premium UI added")
