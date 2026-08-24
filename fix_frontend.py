content = open('index.html', 'r', encoding='utf-8').read()

# Fix loadAnalytics
content = content.replace('''function loadAnalytics() {
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
        }''', '''function loadAnalytics() {
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
        }''')

# Fix loadCalendar
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
            });
        }''', '''function loadCalendar() {
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
        }''')

open('index.html', 'w', encoding='utf-8').write(content)
print("Frontend functions fixed!")
