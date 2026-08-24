with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Modify login success to store token
old_login_success = "localStorage.setItem(\"authToken\", d.token);"
new_login_success = "localStorage.setItem(\"authToken\", d.token);\n                    localStorage.setItem(\"authUser\", JSON.stringify({id: d.id, username: d.username, email: d.email}));"
content = content.replace(old_login_success, new_login_success)

# Modify register success to store token too
old_register_success = "showToast(\"Sign up successful! Please login\", \"success\");"
new_register_success = "if (d.token) { localStorage.setItem(\"authToken\", d.token); localStorage.setItem(\"authUser\", JSON.stringify({id: d.id, username: d.username, email: d.email})); document.getElementById(\"auth-section\").style.display = \"none\"; document.getElementById(\"user-info\").style.display = \"block\"; document.getElementById(\"logged-username\").textContent = d.username; showToast(\"Sign up successful!\", \"success\"); } else { showToast(\"Sign up failed\", \"error\"); }"
content = content.replace(old_register_success, new_register_success)

# Add function to get auth headers
old_toggleSave = 'function toggleSave(id) {'
auth_header_func = '''function getAuthHeaders() {
            var token = localStorage.getItem("authToken");
            return token ? {"Authorization": "Bearer " + token, "Content-Type": "application/json"} : {"Content-Type": "application/json"};
        }
        
        function toggleSave(id) {'''
content = content.replace(old_toggleSave, auth_header_func)

# Update toggleSave to use auth header and call protected endpoint
old_toggle_body = '''function toggleSave(id) {
            var idx = savedTrends.indexOf(id);
            if (idx > -1) { savedTrends.splice(idx,1); showToast("Removed","success"); }
            else { savedTrends.push(id); showToast("Saved","success"); }
            localStorage.setItem("savedTrends", JSON.stringify(savedTrends));
            loadTrends();
        }'''

new_toggle_body = '''function toggleSave(id) {
            var idx = savedTrends.indexOf(id);
            if (idx > -1) { savedTrends.splice(idx,1); showToast("Removed","success"); }
            else { savedTrends.push(id); showToast("Saved","success"); }
            localStorage.setItem("savedTrends", JSON.stringify(savedTrends));
            loadTrends();
            
            var authUser = localStorage.getItem("authUser");
            if (authUser) {
                var user = JSON.parse(authUser);
                fetch(API_URL + "/user/save-trend", {
                    method: "POST",
                    headers: getAuthHeaders(),
                    body: JSON.stringify({user_id: user.id, trend_id: id})
                }).then(function(r){ return r.json(); }).then(function(d){ console.log(d); }).catch(function(){});
            }
        }'''
content = content.replace(old_toggle_body, new_toggle_body)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Frontend JWT integration added")
