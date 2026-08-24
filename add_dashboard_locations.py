import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert region selector and location containers after dashboard page header
old_dashboard_header = '<div id="dashboard" class="page active">\n            <div class="page-header"><h1>Trending Now</h1></div>'
new_dashboard_header = '''<div id="dashboard" class="page active">
            <div class="page-header"><h1>Trending Now</h1></div>
            <div style="display:flex;gap:0.5rem;margin-bottom:1rem;flex-wrap:wrap;align-items:center;">
                <span style="font-weight:bold;color:#333;">📍 Region:</span>
                <select id="dashboard-region-select" class="form-control" style="max-width:220px;display:inline-block;"></select>
                <button class="btn btn-primary" onclick="loadDashboardLocationTrends()">Show My Trends</button>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:2rem;">
                <div>
                    <h3 style="margin-bottom:0.5rem;">Local Trends</h3>
                    <div id="local-trends-dashboard" class="trends-grid"></div>
                </div>
                <div>
                    <h3 style="margin-bottom:0.5rem;">International Trends</h3>
                    <div id="international-trends-dashboard" class="trends-grid"></div>
                </div>
            </div>
            <h3 style="margin-bottom:0.5rem;">All Trends</h3>'''
content = content.replace(old_dashboard_header, new_dashboard_header)

# Add new functions before showToast
old_showtoast = 'function showToast('
new_functions = '''function loadDashboardRegions() {
            var select = document.getElementById("dashboard-region-select");
            fetch(API_URL + "/trends/regions").then(function(r){return r.json();}).then(function(d){
                select.innerHTML = "";
                d.regions.forEach(function(region){
                    select.innerHTML += '<option value="' + region + '">' + region + '</option>';
                });
                // Try to auto-detect from browser language
                var lang = navigator.language || navigator.userLanguage;
                var country = "United States";
                if (lang.indexOf("GB") >= 0) country = "United Kingdom";
                else if (lang.indexOf("ZA") >= 0) country = "South Africa";
                else if (lang.indexOf("NG") >= 0) country = "Nigeria";
                else if (lang.indexOf("KE") >= 0) country = "Kenya";
                else if (lang.indexOf("IN") >= 0) country = "India";
                else if (lang.indexOf("CA") >= 0) country = "Canada";
                else if (lang.indexOf("AU") >= 0) country = "Australia";
                else if (lang.indexOf("BR") >= 0) country = "Brazil";
                else if (lang.indexOf("DE") >= 0) country = "Germany";
                else if (lang.indexOf("FR") >= 0) country = "France";
                select.value = country;
                loadDashboardLocationTrends();
            });
        }
        
        function loadDashboardLocationTrends() {
            var region = document.getElementById("dashboard-region-select").value;
            if (!region) return;
            fetch(API_URL + "/trends/by-region?region=" + encodeURIComponent(region))
                .then(function(r){return r.json();})
                .then(function(d){
                    var localC = document.getElementById("local-trends-dashboard");
                    var intlC = document.getElementById("international-trends-dashboard");
                    localC.innerHTML = "";
                    intlC.innerHTML = "";
                    
                    d.local_trends.forEach(function(t){
                        localC.innerHTML += '<div class="trend-card"><strong>' + t.name + '</strong><br><span style="font-size:0.85rem;color:#666;">Score: ' + Math.round(t.trend_score) + ' | Growth: +' + Math.round(t.growth_rate) + '%</span><br><span style="font-size:0.8rem;color:#10b981;">Top locations: ' + t.top_locations.slice(0,3).join(', ') + '</span></div>';
                    });
                    
                    d.international_trends.forEach(function(t){
                        intlC.innerHTML += '<div class="trend-card"><strong>' + t.name + '</strong><br><span style="font-size:0.85rem;color:#666;">Score: ' + Math.round(t.trend_score) + ' | Growth: +' + Math.round(t.growth_rate) + '%</span><br><span style="font-size:0.8rem;color:#10b981;">Top locations: ' + t.top_locations.slice(0,3).join(', ') + '</span></div>';
                    });
                });
        }
        
        function showToast('''
content = content.replace(old_showtoast, new_functions)

# Call loadDashboardRegions after initial load
old_initial = 'loadTrends();'
new_initial = 'loadTrends();\n        loadDashboardRegions();'
content = content.replace(old_initial, new_initial)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Dashboard location sections added")
