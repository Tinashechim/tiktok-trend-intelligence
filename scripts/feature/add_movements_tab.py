content = open('index.html', 'r', encoding='utf-8').read()

# Add Movements tab after Dashboard
content = content.replace('<button class="nav-link" data-page="analytics"', '<button class="nav-link" data-page="movements" data-tooltip="Detected movement and gesture trends">Movements</button>\n                <button class="nav-link" data-page="analytics"')

# Add movements page div
old_analytics_page = '<div id="analytics" class="page">'
new_movements_page = '''<div id="movements" class="page">
            <div class="page-header"><h1>Movement Trends</h1><p>Automatically detected gestures and movements</p></div>
            <div id="movements-container" class="trends-grid"><div class="loading">Loading...</div></div>
        </div>
        <div id="analytics" class="page">'''
content = content.replace(old_analytics_page, new_movements_page)

# Add movements to nav click handler
content = content.replace('if (page === "analytics") loadAnalytics();', 'if (page === "movements") loadMovements();\n                if (page === "analytics") loadAnalytics();')

# Add loadMovements function
old_showtoast = 'function showToast('
new_loadmovements = '''function loadMovements() {
            var c = document.getElementById("movements-container");
            c.innerHTML = "<div class=loading>Detecting movement patterns...</div>";
            fetch(API_URL + "/trends/movement").then(function(r){return r.json();}).then(function(d){
                if (!d.movement_trends || !d.movement_trends.length) {
                    c.innerHTML = "<div class=loading>No movement trends detected</div>";
                    return;
                }
                var html = "";
                d.movement_trends.forEach(function(m){
                    var strengthColor = m.trend_strength > 60 ? "#10b981" : m.trend_strength > 40 ? "#f59e0b" : "#ef4444";
                    html += "<div style=background:white;padding:1rem;border-radius:10px;>";
                    html += "<strong style=font-size:1.1rem;>" + m.pattern.replace(/_/g, " ") + "</strong>";
                    html += "<div style=margin-top:8px;>";
                    html += "<div style=display:flex;justify-content:space-between;font-size:0.85rem;>";
                    html += "<span>Trend Strength</span>";
                    html += "<span style=font-weight:bold;color:" + strengthColor + ";>" + m.trend_strength + "%</span>";
                    html += "</div>";
                    html += "<div style=height:6px;background:#f0f0f0;border-radius:3px;margin-top:5px;overflow:hidden;>";
                    html += "<div style=height:100%;width:" + m.trend_strength + "%;background:" + strengthColor + ";border-radius:3px;></div>";
                    html += "</div></div>";
                    html += "<p style=color:#666;font-size:0.85rem;margin-top:8px;>" + m.description + "</p>";
                    html += "</div>";
                });
                c.innerHTML = html;
            }).catch(function(){ c.innerHTML = "<div class=loading>Error detecting movements</div>"; });
        }
        
        function showToast('''
content = content.replace(old_showtoast, new_loadmovements)

open('index.html', 'w', encoding='utf-8').write(content)
print("Movements tab added!")
