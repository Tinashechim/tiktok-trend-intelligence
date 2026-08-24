html_file = open('index.html', 'r', encoding='utf-8')
content = html_file.read()
html_file.close()

# Fix loadManage function
old_manage = '''function loadManage() {
            var container = document.getElementById("manage-container");
            container.innerHTML = "<div class=loading>Loading...</div>";
            fetch(API_URL + "/trends/all")
                .then(function(r) { return r.json(); })
                .then(function(trends) {
                    var html = "";
                    trends.forEach(function(t) {
                        html += "<div class=trend-card>";
                        html += "<div class=trend-name>" + t.name + "</div>";
                        html += "<div style=font-size:0.8rem;color:#666;>" + t.type + " | " + Math.round(t.trend_score) + "/100</div>";
                        html += "<button onclick=deleteTrend(" + t.id + ") style=background:#fee2e2;color:#dc2626;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;margin-top:8px;>Delete</button>";
                        html += "</div>";
                    });
                    container.innerHTML = html || "<div class=loading>No trends</div>";
                })
                .catch(function() { container.innerHTML = "<div class=loading>Error</div>"; });
        }'''

new_manage = '''function loadManage() {
            var container = document.getElementById("manage-container");
            container.innerHTML = "<div class=loading>Loading...</div>";
            fetch(API_URL + "/trends/all")
                .then(function(r) { 
                    if (!r.ok) throw new Error("HTTP " + r.status);
                    return r.json(); 
                })
                .then(function(trends) {
                    if (!trends || !trends.length) {
                        container.innerHTML = "<div class=loading>No trends found</div>";
                        return;
                    }
                    var html = "";
                    for (var i = 0; i < trends.length; i++) {
                        var t = trends[i];
                        html += "<div class=trend-card>";
                        html += "<div class=trend-name>" + t.name + "</div>";
                        html += "<div style=font-size:0.8rem;color:#666;margin-bottom:8px;>" + t.type + " | Score: " + Math.round(t.trend_score) + "</div>";
                        html += "<button onclick=\\"deleteTrend(" + t.id + ")\\" style=background:#fee2e2;color:#dc2626;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;>Delete</button>";
                        html += "</div>";
                    }
                    container.innerHTML = html;
                })
                .catch(function(e) { 
                    container.innerHTML = "<div class=loading>Error: " + e.message + "</div>";
                });
        }'''

content = content.replace(old_manage, new_manage)

html_file = open('index.html', 'w', encoding='utf-8')
html_file.write(content)
html_file.close()
print("Manage page fixed!")
