with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace upgradePremium function
old_upgrade = '''function upgradePremium() {
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
        }'''

new_upgrade = '''function upgradePremium() {
            var authUser = localStorage.getItem("authUser");
            if (!authUser) { showToast("Please login first", "error"); return; }
            var user = JSON.parse(authUser);
            fetch(API_URL + "/premium/create-checkout", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({user_id: user.id})
            })
            .then(function(r){ return r.json(); })
            .then(function(d){
                if (d.checkout_url) {
                    window.location.href = d.checkout_url;
                } else {
                    showToast(d.detail || "Stripe not configured", "error");
                }
            })
            .catch(function(){ showToast("Upgrade failed", "error"); });
        }'''

if old_upgrade in content:
    content = content.replace(old_upgrade, new_upgrade)
    print("Upgrade button updated for Stripe")
else:
    print("Could not find upgradePremium function")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Frontend Stripe integration added")
