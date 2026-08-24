html_file = open('index.html', 'r', encoding='utf-8')
content = html_file.read()
html_file.close()

# Add all nav tabs before Refresh button
old_tabs = '<button class="nav-link" onclick="refreshTrends()">Refresh</button>'
new_tabs = '''<button class="nav-link" data-page="analytics">Analytics</button>
                <button class="nav-link" data-page="calendar">Calendar</button>
                <button class="nav-link" data-page="saved">Saved</button>
                <button class="nav-link" data-page="ideas">Ideas</button>
                <button class="nav-link" data-page="profile">Profile</button>
                <button class="nav-link" data-page="admin">Add</button>
                <button class="nav-link" onclick="refreshTrends()">Refresh</button>'''
content = content.replace(old_tabs, new_tabs)

# Add page divs before manage page
old_manage_page = '<div id="manage" class="page">'
new_pages = '''<div id="analytics" class="page">
            <div class="page-header"><h1>Analytics</h1></div>
            <div id="analytics-container" class="trends-grid"><div class="loading">Loading...</div></div>
        </div>
        <div id="calendar" class="page">
            <div class="page-header"><h1>Calendar</h1></div>
            <div id="calendar-container" class="trends-grid"><div class="loading">Loading...</div></div>
        </div>
        <div id="saved" class="page">
            <div class="page-header"><h1>Saved</h1></div>
            <div id="saved-container" class="trends-grid"><div class="loading">Loading...</div></div>
        </div>
        <div id="ideas" class="page">
            <div class="page-header"><h1>Content Ideas</h1></div>
            <select id="trend-select" style="width:100%;padding:0.6rem;border:1px solid #ddd;border-radius:6px;margin-bottom:0.5rem;"><option value="">Select trend</option></select>
            <button onclick="generateIdeas()" style="background:#667eea;color:white;padding:0.6rem 1rem;border:none;border-radius:6px;cursor:pointer;">Generate</button>
            <div id="ideas-container"></div>
        </div>
        <div id="profile" class="page">
            <div class="page-header"><h1>Profile</h1></div>
            <div style="background:white;padding:1rem;border-radius:10px;max-width:400px;">
                <form onsubmit="saveProfile(event)">
                    <input type="text" id="username" placeholder="Username" required style="width:100%;padding:0.6rem;border:1px solid #ddd;border-radius:6px;margin-bottom:0.5rem;">
                    <select id="niche" style="width:100%;padding:0.6rem;border:1px solid #ddd;border-radius:6px;margin-bottom:0.5rem;">
                        <option value="fitness">Fitness</option>
                        <option value="beauty">Beauty</option>
                        <option value="fashion">Fashion</option>
                        <option value="food">Food</option>
                        <option value="gaming">Gaming</option>
                        <option value="tech">Tech</option>
                        <option value="music">Music</option>
                        <option value="travel">Travel</option>
                    </select>
                    <button type="submit" style="background:#667eea;color:white;padding:0.6rem 1rem;border:none;border-radius:6px;cursor:pointer;">Save</button>
                </form>
            </div>
        </div>
        <div id="admin" class="page">
            <div class="page-header"><h1>Add Trend</h1></div>
            <div style="background:white;padding:1rem;border-radius:10px;max-width:400px;">
                <form onsubmit="addTrend(event)">
                    <input type="text" id="trend-name" placeholder="Trend name" required style="width:100%;padding:0.6rem;border:1px solid #ddd;border-radius:6px;margin-bottom:0.5rem;">
                    <select id="trend-type" style="width:100%;padding:0.6rem;border:1px solid #ddd;border-radius:6px;margin-bottom:0.5rem;">
                        <option value="sound">Sound</option>
                        <option value="hashtag">Hashtag</option>
                        <option value="topic">Topic</option>
                        <option value="format">Format</option>
                    </select>
                    <input type="number" id="video-count" placeholder="Video count" style="width:100%;padding:0.6rem;border:1px solid #ddd;border-radius:6px;margin-bottom:0.5rem;">
                    <input type="number" id="growth-rate" placeholder="Growth rate %" style="width:100%;padding:0.6rem;border:1px solid #ddd;border-radius:6px;margin-bottom:0.5rem;">
                    <button type="submit" style="background:#667eea;color:white;padding:0.6rem 1rem;border:none;border-radius:6px;cursor:pointer;">Add</button>
                </form>
            </div>
        </div>
        <div id="manage" class="page">'''
content = content.replace(old_manage_page, new_pages)

# Add functions before showToast
old_showtoast = 'function showToast('
new_functions = '''function loadAnalytics() {
            var c = document.getElementById("analytics-container");
            c.innerHTML = "<div class=loading>Loading...</div>";
            fetch(API_URL + "/trends/current").then(function(r){return r.json();}).then(function(trends){
                var sounds = trends.filter(function(t){return t.type==="sound";}).length;
                var hashtags = trends.filter(function(t){return t.type==="hashtag";}).length;
                var topics = trends.filter(function(t){return t.type==="topic";}).length;
                var html = "<div style=background:white;padding:1rem;border-radius:10px;grid-column:1/-1;>";
                html += "<h3>Total: " + trends.length + "</h3>";
                html += "<p>Sounds: " + sounds + " | Hashtags: " + hashtags + " | Topics: " + topics + "</p>";
                html += "</div>";
                c.innerHTML = html;
            });
        }
        
        function loadCalendar() {
            var c = document.getElementById("calendar-container");
            c.innerHTML = "<div class=loading>Loading...</div>";
            fetch(API_URL + "/calendar/weekly-plan").then(function(r){return r.json();}).then(function(d){
                var html = "";
                d.weekly_plan.forEach(function(day){
                    html += "<div style=background:white;padding:1rem;border-radius:10px;>";
                    html += "<strong>" + day.day + "</strong><br>";
                    html += "<span style=font-size:0.85rem;color:#666;>" + day.trend_name + "</span>";
                    html += "</div>";
                });
                c.innerHTML = html;
            });
        }
        
        function loadSaved() {
            var c = document.getElementById("saved-container");
            c.innerHTML = "<div class=loading>Loading...</div>";
            fetch(API_URL + "/trends/current").then(function(r){return r.json();}).then(function(trends){
                var saved = trends.filter(function(t){return savedTrends.indexOf(t.id)!==-1;});
                if (!saved.length) { c.innerHTML = "<div class=loading>No saved trends</div>"; return; }
                var html = "";
                saved.forEach(function(t){
                    html += "<div style=background:white;padding:1rem;border-radius:10px;><strong>" + t.name + "</strong></div>";
                });
                c.innerHTML = html;
            });
        }
        
        function generateIdeas() {
            var id = document.getElementById("trend-select").value;
            if (!id) { showToast("Select a trend", "error"); return; }
            var c = document.getElementById("ideas-container");
            c.innerHTML = "<div class=loading>Generating...</div>";
            fetch(API_URL + "/trends/current").then(function(r){return r.json();}).then(function(trends){
                var trend = trends.find(function(t){return t.id==id;});
                if (trend) {
                    c.innerHTML = "<div style=background:white;padding:1rem;border-radius:10px;><strong>How to use " + trend.name + "</strong><p style=color:#667eea;>You won't believe this trick!</p></div>";
                }
            });
        }
        
        function saveProfile(event) {
            event.preventDefault();
            var profile = {username: document.getElementById("username").value, niche: document.getElementById("niche").value, follower_count: 0, engagement_rate: 0.05, goals: [], sub_niches: [], interests: []};
            fetch(API_URL + "/user/create", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(profile)})
                .then(function(){ showToast("Saved!", "success"); });
        }
        
        function addTrend(event) {
            event.preventDefault();
            var trend = {trend_name: document.getElementById("trend-name").value, trend_type: document.getElementById("trend-type").value, video_count: parseInt(document.getElementById("video-count").value||"0"), growth_rate: parseFloat(document.getElementById("growth-rate").value||"0")};
            fetch(API_URL + "/admin/trends", {method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(trend)})
                .then(function(){ showToast("Added!", "success"); loadTrends(); });
        }
        
        function showToast('''
content = content.replace(old_showtoast, new_functions)

# Update nav click handler to include new pages
old_click = 'if (page === "dashboard") loadTrends();\n                if (page === "manage") loadManage();'
new_click = '''if (page === "dashboard") loadTrends();
                if (page === "manage") loadManage();
                if (page === "analytics") loadAnalytics();
                if (page === "calendar") loadCalendar();
                if (page === "saved") loadSaved();
                if (page === "ideas") { loadTrendSelect(); }
                if (page === "profile") {}'''
content = content.replace(old_click, new_click)

# Add savedTrends variable
content = content.replace('var API_URL =', 'var savedTrends = JSON.parse(localStorage.getItem("savedTrends") || "[]");\n        var API_URL =')

# Add loadTrendSelect function
old_loadtrends = 'function loadTrends() {'
new_loadtrends = '''function loadTrendSelect() {
            var select = document.getElementById("trend-select");
            fetch(API_URL + "/trends/current").then(function(r){return r.json();}).then(function(trends){
                select.innerHTML = "<option value=>Select</option>";
                trends.forEach(function(t){ select.innerHTML += "<option value=" + t.id + ">" + t.name + "</option>"; });
            });
        }
        
        function loadTrends() {'''
content = content.replace(old_loadtrends, new_loadtrends)

html_file = open('index.html', 'w', encoding='utf-8')
html_file.write(content)
html_file.close()
print("All tabs added back!")
