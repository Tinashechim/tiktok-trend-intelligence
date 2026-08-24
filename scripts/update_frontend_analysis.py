content = open('index.html', 'r', encoding='utf-8').read()

# Add click handler to trend cards to show analysis
# We'll modify displayTrends to add a button that calls showAnalysis(trendId)
old_display = "html += '<button onclick=\"toggleSave(' + t.id + ')\" style=\"margin-top:8px;background:none;border:none;cursor:pointer;\">' + (savedTrends.indexOf(t.id)>-1 ? 'Remove' : 'Save') + '</button>';"
new_display = old_display + "\n                html += '<button onclick=\"showAnalysis(' + t.id + ')\" style=\"margin-top:8px;background:#667eea;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;margin-left:5px;\">Analysis</button>';"
content = content.replace(old_display, new_display)

# Add showAnalysis function before showToast
old_showtoast = 'function showToast('
new_showanalysis = '''
        function showAnalysis(trendId) {
            var modal = document.createElement("div");
            modal.style.position = "fixed";
            modal.style.top = "0";
            modal.style.left = "0";
            modal.style.width = "100%";
            modal.style.height = "100%";
            modal.style.background = "rgba(0,0,0,0.5)";
            modal.style.zIndex = "9999";
            modal.style.display = "flex";
            modal.style.alignItems = "center";
            modal.style.justifyContent = "center";
            modal.innerHTML = '<div style="background:white;border-radius:12px;padding:2rem;max-width:600px;width:90%;max-height:80vh;overflow-y:auto;">' +
                '<h2 style="margin-bottom:1rem;">Trend Analysis</h2>' +
                '<div id="analysis-content">Loading...</div>' +
                '<button onclick="this.closest(\\'div\\').parentElement.remove()" style="margin-top:1rem;background:#ef4444;color:white;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;">Close</button>' +
                '</div>';
            document.body.appendChild(modal);
            
            fetch(API_URL + "/trends/" + trendId + "/analysis")
                .then(function(r){ return r.json(); })
                .then(function(data){
                    var html = "<h3 style=\\"color:#333;\\">" + data.trend + "</h3>";
                    html += "<h4>Top Videos</h4>";
                    data.top_videos.forEach(function(v){
                        html += "<div style=\\"background:#f8fafc;padding:0.8rem;border-radius:8px;margin-bottom:0.5rem;\\">";
                        html += "<strong>" + v.title + "</strong><br>";
                        html += "<span style=\\"font-size:0.85rem;color:#666;\\">Views: " + formatNumber(v.views) + " | Likes: " + formatNumber(v.likes) + "</span><br>";
                        html += "<span style=\\"font-size:0.85rem;color:#10b981;\\">Unique: " + v.unique_factor + "</span>";
                        html += "</div>";
                    });
                    html += "<h4 style=\\"margin-top:1rem;\\">Why It's Trending</h4>";
                    html += "<p style=\\"color:#555;\\">" + data.analysis.why_trending + "</p>";
                    html += "<h4>How to Beat</h4>";
                    html += "<p style=\\"color:#555;\\">" + data.analysis.beat_strategy + "</p>";
                    document.getElementById("analysis-content").innerHTML = html;
                })
                .catch(function(){ document.getElementById("analysis-content").innerHTML = "Error loading analysis"; });
        }
        
        function showToast('''
content = content.replace(old_showtoast, new_showanalysis)

open('index.html', 'w', encoding='utf-8').write(content)
print("Frontend updated with analysis modal")
