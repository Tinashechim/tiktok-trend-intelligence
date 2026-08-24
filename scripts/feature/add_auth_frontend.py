with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add auth section in profile page before TikTok Connect
old_connect = '<h3>Connect TikTok Profile</h3>'
new_auth = '''<h3>Login / Sign Up</h3>
                <div id="auth-section">
                    <input type="text" id="auth-username" placeholder="Username" class="form-control">
                    <input type="email" id="auth-email" placeholder="Email" class="form-control">
                    <input type="password" id="auth-password" placeholder="Password" class="form-control">
                    <button type="button" class="btn btn-primary" onclick="registerUser()">Sign Up</button>
                    <button type="button" class="btn btn-primary" onclick="loginUser()" style="margin-left:0.5rem;">Login</button>
                    <div id="auth-status" style="margin-top:0.5rem;font-size:0.85rem;"></div>
                </div>
                <div id="user-info" style="display:none;">
                    <p>Welcome, <strong id="logged-username"></strong></p>
                    <button class="btn btn-primary" onclick="logoutUser()">Logout</button>
                </div>
                <hr style="margin:1.5rem 0;">
                <h3>Connect TikTok Profile</h3>'''
content = content.replace(old_connect, new_auth)

# Add auth functions before connectTikTok
old_connect_func = 'function connectTikTok() {'
new_auth_functions = '''function registerUser() {
            var username = document.getElementById("auth-username").value;
            var email = document.getElementById("auth-email").value;
            var password = document.getElementById("auth-password").value;
            if (!username || !email || !password) { showToast("Fill all fields", "error"); return; }
            fetch(API_URL + "/auth/register", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username: username, email: email, password: password})
            })
            .then(function(r){ return r.json(); })
            .then(function(d){
                if (d.id) { showToast("Sign up successful! Please login", "success"); }
                else { showToast(d.detail || "Error", "error"); }
            })
            .catch(function(){ showToast("Sign up failed", "error"); });
        }
        
        function loginUser() {
            var email = document.getElementById("auth-email").value;
            var password = document.getElementById("auth-password").value;
            if (!email || !password) { showToast("Enter email and password", "error"); return; }
            fetch(API_URL + "/auth/login", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({email: email, password: password})
            })
            .then(function(r){ return r.json(); })
            .then(function(d){
                if (d.token) {
                    localStorage.setItem("authToken", d.token);
                    localStorage.setItem("authUser", JSON.stringify(d));
                    document.getElementById("auth-section").style.display = "none";
                    document.getElementById("user-info").style.display = "block";
                    document.getElementById("logged-username").textContent = d.username;
                    showToast("Login successful!", "success");
                } else {
                    showToast(d.detail || "Login failed", "error");
                }
            })
            .catch(function(){ showToast("Login failed", "error"); });
        }
        
        function logoutUser() {
            localStorage.removeItem("authToken");
            localStorage.removeItem("authUser");
            document.getElementById("auth-section").style.display = "block";
            document.getElementById("user-info").style.display = "none";
            showToast("Logged out", "success");
        }
        
        function checkAuth() {
            var authUser = localStorage.getItem("authUser");
            if (authUser) {
                var user = JSON.parse(authUser);
                document.getElementById("auth-section").style.display = "none";
                document.getElementById("user-info").style.display = "block";
                document.getElementById("logged-username").textContent = user.username;
            } else {
                document.getElementById("auth-section").style.display = "block";
                document.getElementById("user-info").style.display = "none";
            }
        }
        
        function connectTikTok() {'''
content = content.replace(old_connect_func, new_auth_functions)

# Call checkAuth on initial load
content = content.replace('loadDashboardRegions();', 'loadDashboardRegions();\n        checkAuth();')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Auth UI added")
