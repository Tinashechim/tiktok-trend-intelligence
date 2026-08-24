import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Locations tab after Movements in nav
content = content.replace(
    '<button class="nav-link" data-page="movements" title="Detected gesture and movement trends">Movements</button>',
    '<button class="nav-link" data-page="movements" title="Detected gesture and movement trends">Movements</button>\n                <button class="nav-link" data-page="locations" title="Trending locations and local trends">Locations</button>'
)

# Add Locations page before movements page
old_movements_page = '<div id="movements" class="page">'
new_locations_page = '''<div id="locations" class="page">
            <div class="page-header"><h1>Trending Locations</h1><p>See local and international trends by region</p></div>
            <div style="margin-bottom:1rem;">
                <select id="region-select" class="form-control" style="max-width:300px;display:inline-block;"></select>
                <button class="btn btn-primary" onclick="loadLocationTrends()">Show Trends</button>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                <div>
                    <h3>Local Trends</h3>
                    <div id="local-trends" class="trends-grid"></div>
                </div>
                <div>
                    <h3>International Trends</h3>
                    <div id="international-trends" class="trends-grid"></div>
                </div>
            </div>
        </div>
        <div id="movements" class="page">'''
content = content.replace(old_movements_page, new_locations_page)

# Add location handler in nav click
content = content.replace(
    'if (page === "movements") loadMovements();',
    'if (page === "movements") loadMovements();\n                if (page === "locations") loadRegions();'
)

# Add functions for locations before showToast
old_showtoast = 'function showToast('
new_location_functions = '''function loadRegions() {
            var select = document.getElementById("region-select");
            fetch(API_URL + "/trends/regions").then(function(r){return r.json();}).then(function(d){
                select.innerHTML = "";
                d.regions.forEach(function(region){
                    select.innerHTML += '<option value="' + region + '">' + region + '</option>';
                });
                // Default to first
                if (d.regions.length) loadLocationTrends();
            });
        }
        
        function loadLocationTrends() {
            var region = document.getElementById("region-select").value;
            if (!region) return;
            fetch(API_URL + "/trends/by-region?region=" + encodeURIComponent(region))
                .then(function(r){return r.json();})
                .then(function(d){
                    var localC = document.getElementById("local-trends");
                    var intlC = document.getElementById("international-trends");
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
content = content.replace(old_showtoast, new_location_functions)

# Update showAnalysis to include top locations
# We'll insert location fetch after modal content loaded
# Find where analysis-content innerHTML is set, add location section
old_analysis_end = "document.getElementById(\"analysis-content\").innerHTML = html;"
new_analysis_end = '''document.getElementById("analysis-content").innerHTML = html;
            
            // Fetch and display top locations
            fetch(API_URL + "/trends/" + trendId + "/locations")
                .then(function(r){ return r.json(); })
                .then(function(locData){
                    var locHtml = "<div style=\\"background:#f8fafc;padding:1rem;border-radius:8px;margin-bottom:1rem;\\">";
                    locHtml += "<h3 style=\\"color:#333;margin-bottom:0.5rem;\\">📍 Top Trending Locations</h3>";
                    locData.top_locations.forEach(function(loc){
                        locHtml += "<span style=\\"display:inline-block;background:#e0e7ff;color:#4f46e5;padding:3px 10px;border-radius:15px;margin:3px;font-size:0.85rem;\\">" + loc + "</span>";
                    });
                    if (locData.is_international) {
                        locHtml += "<p style=\\"color:#10b981;margin-top:8px;\\">🌍 This is an international trend</p>";
                    } else {
                        locHtml += "<p style=\\"color:#f59e0b;margin-top:8px;\\">📍 This is a local/regional trend</p>";
                    }
                    locHtml += "</div>";
                    var analysisContent = document.getElementById("analysis-content");
                    analysisContent.innerHTML += locHtml;
                })
                .catch(function(){});'''
content = content.replace(old_analysis_end, new_analysis_end)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Frontend updated with locations tab and analysis locations")
