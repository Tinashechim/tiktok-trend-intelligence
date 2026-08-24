html_file = open('index.html', 'w', encoding='utf-8')
html_file.write('''<!DOCTYPE html>
<html>
<head>
    <title>TrendPilot - TikTok Intelligence</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Segoe UI", Arial, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        .navbar {
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0.8rem 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .nav-brand {
            font-size: 1.3rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .nav-links { display: flex; gap: 0.3rem; flex-wrap: wrap; }
        .nav-link {
            padding: 0.4rem 0.7rem;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 0.8rem;
            color: #666;
            border-radius: 6px;
            transition: all 0.3s;
        }
        .nav-link:hover { background: #f0f0f0; }
        .nav-link.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        .main-container {
            max-width: 1200px;
            margin: 1.5rem auto;
            padding: 0 1rem;
        }
        .page { display: none; }
        .page.active { display: block; animation: fadeIn 0.3s; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .page-header { margin-bottom: 1.5rem; }
        .page-header h1 { font-size: 1.5rem; color: #333; }
        .page-header p { color: #666; font-size: 0.9rem; }
        
        .trends-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1rem;
        }
        .trend-card {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            position: relative;
        }
        .trend-stage {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 15px;
            font-size: 0.7rem;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .trend-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .trend-type {
            background: #e0e7ff;
            color: #4f46e5;
            padding: 3px 8px;
            border-radius: 15px;
            font-size: 0.7rem;
            font-weight: bold;
            text-transform: uppercase;
        }
        .trend-score { font-size: 1.2rem; font-weight: bold; color: #667eea; }
        .trend-name { font-size: 1rem; font-weight: bold; color: #333; margin-bottom: 10px; }
        .trend-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            background: #f8fafc;
            padding: 10px;
            border-radius: 8px;
        }
        .metric { text-align: center; }
        .metric-value { font-weight: bold; color: #333; font-size: 0.9rem; }
        .metric-label { font-size: 0.7rem; color: #666; }
        
        .admin-form {
            background: white;
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 500px;
            margin-bottom: 2rem;
        }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; font-weight: bold; margin-bottom: 0.3rem; font-size: 0.9rem; }
        .form-control {
            width: 100%;
            padding: 0.6rem;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 0.9rem;
        }
        .btn {
            padding: 0.6rem 1.2rem;
            border: none;
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: bold;
            cursor: pointer;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        .btn-danger {
            background: #ef4444;
            color: white;
        }
        .btn-small {
            padding: 0.3rem 0.6rem;
            font-size: 0.75rem;
        }
        .delete-btn {
            position: absolute;
            bottom: 0.8rem;
            right: 0.8rem;
            background: #fee2e2;
            color: #dc2626;
            border: none;
            border-radius: 4px;
            padding: 3px 8px;
            cursor: pointer;
            font-size: 0.7rem;
        }
        .loading { text-align: center; padding: 2rem; color: #666; }
        
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 0.8rem 1.2rem;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 1000;
            animation: slideIn 0.3s;
        }
        .toast.success { background: #10b981; }
        .toast.error { background: #ef4444; }
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand">TrendPilot</div>
            <div class="nav-links">
                <button class="nav-link active" data-page="dashboard">Dashboard</button>
                <button class="nav-link" data-page="admin">Add Trends</button>
                <button class="nav-link" data-page="manage">Manage</button>
            </div>
        </div>
    </nav>
    
    <div class="main-container">
        <div id="dashboard" class="page active">
            <div class="page-header">
                <h1>All Trends</h1>
                <p>Current trending content</p>
            </div>
            <div id="trends-container" class="trends-grid">
                <div class="loading">Loading...</div>
            </div>
        </div>
        
        <div id="admin" class="page">
            <div class="page-header">
                <h1>Add New Trend</h1>
                <p>Manually enter trending content you find on TikTok</p>
            </div>
            <div class="admin-form">
                <form onsubmit="addTrend(event)">
                    <div class="form-group">
                        <label>Trend Name</label>
                        <input type="text" id="trend-name" class="form-control" required placeholder="e.g., #newtrend or Song Name">
                    </div>
                    <div class="form-group">
                        <label>Trend Type</label>
                        <select id="trend-type" class="form-control">
                            <option value="sound">Sound</option>
                            <option value="hashtag">Hashtag</option>
                            <option value="topic">Topic</option>
                            <option value="format">Format</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Video Count</label>
                        <input type="number" id="video-count" class="form-control" min="0" placeholder="e.g., 50000">
                    </div>
                    <div class="form-group">
                        <label>Growth Rate (%)</label>
                        <input type="number" id="growth-rate" class="form-control" min="0" placeholder="e.g., 250">
                    </div>
                    <div class="form-group">
                        <label>Competition Level</label>
                        <select id="competition" class="form-control">
                            <option value="Very Low">Very Low</option>
                            <option value="Low">Low</option>
                            <option value="Medium">Medium</option>
                            <option value="High">High</option>
                            <option value="Very High">Very High</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Trend Stage</label>
                        <select id="stage" class="form-control">
                            <option value="🚀 Early">🚀 Early</option>
                            <option value="🔥 Emerging">🔥 Emerging</option>
                            <option value="📈 Rising">📈 Rising</option>
                            <option value="Peak">Peak</option>
                            <option value="📉 Declining">📉 Declining</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Add Trend</button>
                </form>
            </div>
        </div>
        
        <div id="manage" class="page">
            <div class="page-header">
                <h1>Manage Trends</h1>
                <p>Delete trends that are no longer relevant</p>
            </div>
            <div id="manage-container" class="trends-grid">
                <div class="loading">Loading...</div>
            </div>
        </div>
    </div>
    
    <script>
        const API_URL = "https://tiktok-trend-intelligence.onrender.com/api";
        
        document.querySelectorAll(".nav-link").forEach(function(link) {
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
        
        async function loadTrends() {
            const container = document.getElementById("trends-container");
            container.innerHTML = "<div class=loading>Loading...</div>";
            try {
                const response = await fetch(API_URL + "/trends/current");
                const trends = await response.json();
                displayTrends(container, trends);
            } catch (error) {
                container.innerHTML = "<div class=loading>Error loading trends</div>";
            }
        }
        
        async function loadManage() {
            const container = document.getElementById("manage-container");
            container.innerHTML = "<div class=loading>Loading...</div>";
            try {
                const response = await fetch(API_URL + "/trends/all");
                const trends = await response.json();
                displayManage(container, trends);
            } catch (error) {
                container.innerHTML = "<div class=loading>Error loading</div>";
            }
        }
        
        function displayTrends(container, trends) {
            if (!trends.length) {
                container.innerHTML = "<div class=loading>No trends found</div>";
                return;
            }
            var html = "";
            trends.forEach(function(trend) {
                var stageStyle = getStageStyle(trend.trend_stage);
                html += "<div class=trend-card>";
                html += "<span class=trend-stage style=" + stageStyle + ">" + trend.trend_stage + "</span>";
                html += "<div class=trend-header>";
                html += "<span class=trend-type>" + trend.type + "</span>";
                html += "<span class=trend-score>" + Math.round(trend.trend_score) + "/100</span>";
                html += "</div>";
                html += "<div class=trend-name>" + trend.name + "</div>";
                html += "<div class=trend-metrics>";
                html += "<div class=metric><div class=metric-value>" + (trend.growth_rate > 0 ? "+" : "") + Math.round(trend.growth_rate) + "%</div><div class=metric-label>Growth</div></div>";
                html += "<div class=metric><div class=metric-value>" + trend.competition_level + "</div><div class=metric-label>Competition</div></div>";
                html += "<div class=metric><div class=metric-value>" + formatNumber(trend.video_count) + "</div><div class=metric-label>Videos</div></div>";
                html += "</div></div>";
            });
            container.innerHTML = html;
        }
        
        function displayManage(container, trends) {
            if (!trends.length) {
                container.innerHTML = "<div class=loading>No trends found</div>";
                return;
            }
            var html = "";
            trends.forEach(function(trend) {
                html += "<div class=trend-card>";
                html += "<div class=trend-name>" + trend.name + "</div>";
                html += "<div style=font-size:0.8rem;color:#666;margin-bottom:8px;>" + trend.type + " | Score: " + Math.round(trend.trend_score) + "</div>";
                html += "<button class=delete-btn onclick=deleteTrend(" + trend.id + ")>Delete</button>";
                html += "</div>";
            });
            container.innerHTML = html;
        }
        
        async function addTrend(event) {
            event.preventDefault();
            
            var trend = {
                trend_name: document.getElementById("trend-name").value,
                trend_type: document.getElementById("trend-type").value,
                video_count: parseInt(document.getElementById("video-count").value || "0"),
                growth_rate: parseFloat(document.getElementById("growth-rate").value || "0"),
                competition_level: document.getElementById("competition").value,
                trend_stage: document.getElementById("stage").value,
                engagement_rate: 5000
            };
            
            try {
                const response = await fetch(API_URL + "/admin/trends", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(trend)
                });
                
                if (response.ok) {
                    showToast("Trend added successfully!", "success");
                    document.getElementById("trend-name").value = "";
                    document.getElementById("video-count").value = "";
                    document.getElementById("growth-rate").value = "";
                    loadTrends();
                } else {
                    showToast("Error adding trend", "error");
                }
            } catch (error) {
                showToast("Error connecting to server", "error");
            }
        }
        
        async function deleteTrend(trendId) {
            if (!confirm("Delete this trend?")) return;
            
            try {
                const response = await fetch(API_URL + "/admin/trends/" + trendId, {
                    method: "DELETE"
                });
                
                if (response.ok) {
                    showToast("Trend deleted!", "success");
                    loadManage();
                } else {
                    showToast("Error deleting", "error");
                }
            } catch (error) {
                showToast("Error connecting", "error");
            }
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
        
        function showToast(message, type) {
            var toast = document.createElement("div");
            toast.className = "toast " + type;
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(function() { toast.remove(); }, 3000);
        }
        
        loadTrends();
    </script>
</body>
</html>''')
html_file.close()
print("Admin panel created!")
