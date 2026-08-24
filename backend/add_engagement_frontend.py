with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add nav button for engagement after Analytics
old_nav_analytics = '<button class="nav-link" data-page="analytics" title="Trend statistics">Analytics</button>'
new_nav = old_nav_analytics + '\n                <button class="nav-link" data-page="engagement" title="User behavior and engagement stats">Engagement</button>'
content = content.replace(old_nav_analytics, new_nav)

# Add engagement page div before analytics page
old_analytics_page = '<div id="analytics" class="page">'
new_engagement_page = '''<div id="engagement" class="page">
            <div class="page-header"><h1>Engagement Dashboard</h1><p>Real user behavior per trend</p></div>
            <div id="engagement-container" class="trends-grid"><div class="loading">Loading...</div></div>
        </div>
        <div id="analytics" class="page">'''
content = content.replace(old_analytics_page, new_engagement_page)

# Add page navigation handler
old_click_handler = "if (page === \"analytics\") loadAnalytics();"
new_click_handler = "if (page === \"engagement\") loadEngagement();\n                if (page === \"analytics\") loadAnalytics();"
content = content.replace(old_click_handler, new_click_handler)

# Add loadEngagement function before showToast
old_showtoast = 'function showToast('
new_engagement_func = '''function loadEngagement() {
            var c = document.getElementById("engagement-container");
            c.innerHTML = "<div class=loading>Loading engagement data...</div>";
            fetch(API_URL + "/engagement/overview")
                .then(function(r){ return r.json(); })
                .then(function(d){
                    if (!d.engagement || !d.engagement.length) {
                        c.innerHTML = "<div class=loading>No engagement data yet. Interact with trends to generate data.</div>";
                        return;
                    }
                    var html = "";
                    d.engagement.forEach(function(e){
                        html += '<div class="trend-card">';
                        html += '<strong>' + e.trend_name + '</strong>';
                        html += '<div style="margin-top:8px;font-size:0.9rem;">';
                        html += '<div>Total Interactions: <strong>' + e.total_interactions + '</strong></div>';
                        html += '<div>Saves: <strong>' + e.saves + '</strong> | Analysis Views: <strong>' + e.analysis_views + '</strong></div>';
                        html += '<div>Unique Users: <strong>' + e.unique_users + '</strong> | Recurring Users: <strong>' + e.recurring_users + '</strong></div>';
                        html += '<div>Engagement Score: <strong>' + e.engagement_score + '</strong></div>';
                        html += '</div></div>';
                    });
                    c.innerHTML = html;
                })
                .catch(function(){ c.innerHTML = "<div class=loading>Error loading engagement</div>"; });
        }
        
        function showToast('''
content = content.replace(old_showtoast, new_engagement_func)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Engagement dashboard added to frontend")
