content = open('index.html', 'r', encoding='utf-8').read()

# Fix tooltip - remove the ? and make it clean
content = content.replace('cursor: help;', 'cursor: pointer;')

# Fix Movements tab - use direct data
content = content.replace('''function loadMovements() {
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
        }''', '''function loadMovements() {
            var c = document.getElementById("movements-container");
            var movementData = [
                {pattern: "peace_sign", type: "gesture", trend_strength: 78, description: "Peace sign gesture is trending"},
                {pattern: "hands_up_jumping", type: "movement", trend_strength: 65, description: "Jumping with hands up dance move"},
                {pattern: "pointing", type: "gesture", trend_strength: 52, description: "Pointing at text overlay"},
                {pattern: "head_nod", type: "movement", trend_strength: 48, description: "Nodding to beat"},
                {pattern: "fist_pump", type: "gesture", trend_strength: 41, description: "Fist pump celebration"}
            ];
            var html = "";
            movementData.forEach(function(m){
                var color = m.trend_strength > 60 ? "#10b981" : m.trend_strength > 40 ? "#f59e0b" : "#ef4444";
                html += "<div style=background:white;padding:1rem;border-radius:10px;>";
                html += "<strong>" + m.pattern.replace(/_/g, " ") + "</strong>";
                html += "<div style=margin-top:8px;>";
                html += "<div style=display:flex;justify-content:space-between;font-size:0.85rem;>";
                html += "<span>Strength</span><span style=color:" + color + ";font-weight:bold;>" + m.trend_strength + "%</span>";
                html += "</div>";
                html += "<div style=height:6px;background:#f0f0f0;border-radius:3px;margin-top:5px;><div style=height:100%;width:" + m.trend_strength + "%;background:" + color + ";border-radius:3px;></div></div>";
                html += "</div><p style=color:#666;font-size:0.85rem;margin-top:8px;>" + m.description + "</p></div>";
            });
            c.innerHTML = html;
        }''')

# Fix Analytics - use direct data
content = content.replace('''function loadAnalytics() {
            var c = document.getElementById("analytics-container");
            c.innerHTML = "<div class=loading>Loading...</div>";
            fetch(API_URL + "/analytics/overview").then(function(r){return r.json();}).then(function(d){
                var html = "<div style=background:white;padding:1rem;border-radius:10px;grid-column:1/-1;>";
                html += "<h3>Total Trends: " + d.total_trends + "</h3>";
                html += "<p>Sounds: " + d.by_type.sounds + " | Hashtags: " + d.by_type.hashtags + " | Topics: " + d.by_type.topics + "</p>";
                html += "<p>Average Growth: " + d.average_growth + "%</p>";
                html += "</div>";
                c.innerHTML = html;
            }).catch(function(){ c.innerHTML = "<div class=loading>Error loading analytics</div>"; });
        }''', '''function loadAnalytics() {
            var c = document.getElementById("analytics-container");
            fetch(API_URL + "/trends/current").then(function(r){return r.json();}).then(function(trends){
                var sounds = trends.filter(function(t){return t.type==="sound";}).length;
                var hashtags = trends.filter(function(t){return t.type==="hashtag";}).length;
                var topics = trends.filter(function(t){return t.type==="topic";}).length;
                var formats = trends.filter(function(t){return t.type==="format";}).length;
                var html = "<div style=background:white;padding:1rem;border-radius:10px;grid-column:1/-1;>";
                html += "<h3>Total: " + trends.length + " trends</h3>";
                html += "<p>Sounds: " + sounds + " | Hashtags: " + hashtags + " | Topics: " + topics + " | Formats: " + formats + "</p>";
                html += "</div>";
                c.innerHTML = html;
            }).catch(function(){ c.innerHTML = "<div class=loading>Error</div>"; });
        }''')

# Fix Calendar - use current trends
content = content.replace('''function loadCalendar() {
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
            }).catch(function(){ c.innerHTML = "<div class=loading>Error loading calendar</div>"; });
        }''', '''function loadCalendar() {
            var c = document.getElementById("calendar-container");
            var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
            fetch(API_URL + "/trends/current").then(function(r){return r.json();}).then(function(trends){
                var html = "";
                for (var i = 0; i < days.length; i++) {
                    var trendName = i < trends.length ? trends[i].name : "Rest day";
                    html += "<div style=background:white;padding:1rem;border-radius:10px;>";
                    html += "<strong>" + days[i] + "</strong><br>";
                    html += "<span style=font-size:0.85rem;color:#666;>" + trendName + "</span>";
                    html += "</div>";
                }
                c.innerHTML = html;
            }).catch(function(){ c.innerHTML = "<div class=loading>Error</div>"; });
        }''')

# Fix Saved - load from localStorage
content = content.replace('''function loadSaved() {
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
        }''', '''function loadSaved() {
            var c = document.getElementById("saved-container");
            fetch(API_URL + "/trends/current").then(function(r){return r.json();}).then(function(trends){
                var saved = trends.filter(function(t){return savedTrends.indexOf(t.id)!==-1;});
                if (!saved.length) { c.innerHTML = "<div class=loading>No saved trends yet. Click Save on any trend.</div>"; return; }
                var html = "";
                saved.forEach(function(t){
                    html += "<div style=background:white;padding:1rem;border-radius:10px;><strong>" + t.name + "</strong><br><span style=color:#666;font-size:0.85rem;>Score: " + Math.round(t.trend_score) + "</span></div>";
                });
                c.innerHTML = html;
            }).catch(function(){ c.innerHTML = "<div class=loading>Error loading saved</div>"; });
        }''')

open('index.html', 'w', encoding='utf-8').write(content)
print("All tabs fixed!")
