html_file = open('index.html', 'w', encoding='utf-8')
html_file.write('''<!DOCTYPE html>
<html>
<head>
    <title>TrendPilot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f5f7fa; min-height: 100vh; }
        .navbar { background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 0.5rem 1rem; }
        .nav-container { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; gap: 0.5rem; }
        .nav-brand { font-size: 1.2rem; font-weight: bold; color: #667eea; flex-shrink: 0; }
        .nav-links { display: flex; gap: 0.3rem; overflow-x: auto; flex: 1; }
        .nav-link { padding: 0.5rem 0.8rem; border: none; background: none; cursor: pointer; font-size: 0.8rem; color: #666; border-radius: 6px; flex-shrink: 0; }
        .nav-link:hover { background: #f0f0f0; }
        .nav-link.active { background: #667eea; color: white; }
        .main-container { max-width: 1200px; margin: 1.5rem auto; padding: 0 1rem; }
        .page { display: none; }
        .page.active { display: block; }
        .page-header { margin-bottom: 1rem; }
        .page-header h1 { font-size: 1.4rem; color: #333; }
        .trends-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 1rem; }
        .trend-card { background: white; border-radius: 10px; padding: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .trend-stage { display: inline-block; padding: 3px 8px; border-radius: 15px; font-size: 0.7rem; font-weight: bold; margin-bottom: 8px; }
        .trend-header { display: flex; justify-content: space-between; margin-bottom: 8px; }
        .trend-type { background: #e0e7ff; color: #4f46e5; padding: 3px 8px; border-radius: 15px; font-size: 0.7rem; font-weight: bold; }
        .trend-score { font-size: 1.1rem; font-weight: bold; color: #667eea; }
        .trend-name { font-weight: bold; color: #333; margin-bottom: 8px; }
        .trend-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; background: #f8fafc; padding: 8px; border-radius: 8px; }
        .metric { text-align: center; }
        .metric-value { font-weight: bold; font-size: 0.85rem; }
        .metric-label { font-size: 0.7rem; color: #666; }
        .loading { text-align: center; padding: 2rem; color: #666; }
        .toast { position: fixed; bottom: 20px; right: 20px; padding: 0.8rem 1.2rem; border-radius: 8px; color: white; font-weight: bold; z-index: 1000; }
        .toast.success { background: #10b981; }
        .toast.error { background: #ef4444; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand">TrendPilot</div>
            <div class="nav-links">
                <button class="nav-link active" data-page="dashboard">Dashboard</button>
                <button class="nav-link" data-page="manage">Manage</button>
                <button class="nav-link" onclick="refreshTrends()">Refresh</button>
            </div>
        </div>
    </nav>
    
    <div class="main-container">
        <div id="dashboard" class="page active">
            <div class="page-header"><h1>All Trends</h1></div>
            <div id="trends-container" class="trends-grid"><div class="loading">Loading...</div></div>
        </div>
        <div id="manage" class="page">
            <div class="page-header"><h1>Manage</h1></div>
            <div id="manage-container" class="trends-grid"><div class="loading">Loading...</div></div>
        </div>
    </div>
    
    <script>
        var API_URL = "https://tiktok-trend-intelligence.onrender.com/api";
        
        document.querySelectorAll(".nav-link[data-page]").forEach(function(link) {
            link.addEventListener("click", function() {
                var page = this.dataset.page;
                document.querySelectorAll(".nav-link").forEach(function(l) { l.classList.remove("active"); });
                this.classList.add("active");
                document.querySelectorAll(".page").forEach(function(p) { p.classList.remove("active"); });
                document.getElementById(page).classList.add("active");
                if (page === "dashboard") loadTrends();
                if (page === "manage") loadManage();
            });
        });
        
        function loadTrends() {
            var container = document.getElementById("trends-container");
            container.innerHTML = "<div class=loading>Loading...</div>";
            fetch(API_URL + "/trends/current")
                .then(function(r) { return r.json(); })
                .then(function(trends) {
                    if (!trends.length) { container.innerHTML = "<div class=loading>No trends</div>"; return; }
                    var html = "";
                    trends.forEach(function(t) {
                        var stageStyle = getStageStyle(t.trend_stage);
                        html += "<div class=trend-card>";
                        html += "<span class=trend-stage style=" + stageStyle + ">" + t.trend_stage + "</span>";
                        html += "<div class=trend-header>";
                        html += "<span class=trend-type>" + t.type + "</span>";
                        html += "<span class=trend-score>" + Math.round(t.trend_score) + "/100</span>";
                        html += "</div>";
                        html += "<div class=trend-name>" + t.name + "</div>";
                        html += "<div class=trend-metrics>";
                        html += "<div class=metric><div class=metric-value>" + (t.growth_rate > 0 ? "+" : "") + Math.round(t.growth_rate) + "%</div><div class=metric-label>Growth</div></div>";
                        html += "<div class=metric><div class=metric-value>" + t.competition_level + "</div><div class=metric-label>Competition</div></div>";
                        html += "<div class=metric><div class=metric-value>" + formatNumber(t.video_count) + "</div><div class=metric-label>Videos</div></div>";
                        html += "</div></div>";
                    });
                    container.innerHTML = html;
                })
                .catch(function() { container.innerHTML = "<div class=loading>Error loading trends</div>"; });
        }
        
        function loadManage() {
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
        }
        
        function deleteTrend(id) {
            if (!confirm("Delete this trend?")) return;
            fetch(API_URL + "/admin/trends/" + id, { method: "DELETE" })
                .then(function() { loadManage(); showToast("Deleted!", "success"); });
        }
        
        function refreshTrends() {
            showToast("Fetching trends...", "success");
            fetch(API_URL + "/refresh", { method: "POST" })
                .then(function(r) { return r.json(); })
                .then(function(d) { showToast("Updated " + d.count + " trends!", "success"); loadTrends(); })
                .catch(function() { showToast("Error refreshing", "error"); });
        }
        
        function getStageStyle(stage) {
            if (stage.indexOf("Early") >= 0) return "background:#fef3c7;color:#d97706;";
            if (stage.indexOf("Emerging") >= 0) return "background:#fee2e2;color:#dc2626;";
            if (stage.indexOf("Rising") >= 0) return "background:#e0e7ff;color:#4f46e5;";
            if (stage.indexOf("Peak") >= 0) return "background:#d1fae5;color:#059669;";
            return "background:#f3f4f6;color:#6b7280;";
        }
        
        function formatNumber(num) {
            if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
            if (num >= 1000) return (num / 1000).toFixed(1) + "K";
            return Math.round(num).toString();
        }
        
        function showToast(msg, type) {
            var toast = document.createElement("div");
            toast.className = "toast " + type;
            toast.textContent = msg;
            document.body.appendChild(toast);
            setTimeout(function() { toast.remove(); }, 3000);
        }
        
        loadTrends();
    </script>
</body>
</html>''')
html_file.close()
print("Clean dashboard created!")
