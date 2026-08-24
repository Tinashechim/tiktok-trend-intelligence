html_content = open('index.html', 'w', encoding='utf-8')
html_content.write('''<!DOCTYPE html>
<html>
<head>
    <title>TikTok Trend Intelligence</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-box {
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label { color: #666; margin-top: 5px; }
        .trends-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }
        .trend-card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }
        .trend-card:hover { transform: translateY(-5px); }
        .trend-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .trend-type {
            background: #e0e7ff;
            color: #4f46e5;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            text-transform: uppercase;
        }
        .trend-score {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }
        .trend-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }
        .trend-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            background: #f8fafc;
            padding: 15px;
            border-radius: 10px;
        }
        .trend-stat { text-align: center; }
        .trend-stat-value { font-weight: bold; color: #333; }
        .trend-stat-label { font-size: 0.8em; color: #666; }
        .stage {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .loading { text-align: center; color: white; font-size: 1.2em; padding: 50px; }
        .error {
            background: #fee;
            color: #c33;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            color: #667eea;
            border: none;
            padding: 15px 25px;
            border-radius: 50px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }
        .refresh-btn:hover { transform: scale(1.1); }
    </style>
</head>
<body>
    <div class="container">
        <h1>TikTok Trend Intelligence</h1>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value" id="total-trends">0</div>
                <div class="stat-label">Active Trends</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="top-score">0</div>
                <div class="stat-label">Top Score</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="avg-growth">0%</div>
                <div class="stat-label">Avg Growth Rate</div>
            </div>
        </div>
        
        <div id="trends-container">
            <div class="loading">Loading trends...</div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="loadTrends()">Refresh</button>
    
    <script>
        const API_URL = "http://localhost:8001/api";
        
        async function loadTrends() {
            const container = document.getElementById("trends-container");
            container.innerHTML = "<div class=loading>Loading trends...</div>";
            
            try {
                const response = await fetch(API_URL + "/trends/current");
                if (!response.ok) throw new Error("Server returned " + response.status);
                
                const trends = await response.json();
                updateStats(trends);
                displayTrends(trends);
            } catch (error) {
                container.innerHTML = "<div class=error>Error loading trends. Make sure the server is running on port 8001</div>";
            }
        }
        
        function updateStats(trends) {
            if (!trends.length) return;
            document.getElementById("total-trends").textContent = trends.length;
            const topScore = Math.max.apply(null, trends.map(function(t) { return t.trend_score; }));
            document.getElementById("top-score").textContent = Math.round(topScore);
            const avgGrowth = trends.reduce(function(sum, t) { return sum + t.growth_rate; }, 0) / trends.length;
            document.getElementById("avg-growth").textContent = Math.round(avgGrowth) + "%";
        }
        
        function displayTrends(trends) {
            const container = document.getElementById("trends-container");
            
            if (!trends.length) {
                container.innerHTML = "<div class=loading>No trends found</div>";
                return;
            }
            
            const stageColors = {
                "Early": "background:#fef3c7;color:#d97706;",
                "Emerging": "background:#fee2e2;color:#dc2626;",
                "Rising": "background:#e0e7ff;color:#4f46e5;",
                "Peak": "background:#d1fae5;color:#059669;",
                "Declining": "background:#f3f4f6;color:#6b7280;"
            };
            
            var html = "<div class=trends-grid>";
            for (var i = 0; i < trends.length; i++) {
                var trend = trends[i];
                var stageName = trend.trend_stage.replace("🚀 ", "").replace("🔥 ", "").replace("📈 ", "").replace("📉 ", "");
                var stageStyle = stageColors[stageName] || "background:#e0e7ff;color:#4f46e5;";
                
                html += "<div class=trend-card>";
                html += "<span class=stage style=" + stageStyle + ">" + trend.trend_stage + "</span>";
                html += "<div class=trend-header>";
                html += "<span class=trend-type>" + trend.type + "</span>";
                html += "<span class=trend-score>" + Math.round(trend.trend_score) + "/100</span>";
                html += "</div>";
                html += "<div class=trend-name>" + trend.name + "</div>";
                html += "<div class=trend-stats>";
                html += "<div class=trend-stat><div class=trend-stat-value>" + (trend.growth_rate > 0 ? "+" : "") + Math.round(trend.growth_rate) + "%</div><div class=trend-stat-label>Growth</div></div>";
                html += "<div class=trend-stat><div class=trend-stat-value>" + trend.competition_level + "</div><div class=trend-stat-label>Competition</div></div>";
                html += "<div class=trend-stat><div class=trend-stat-value>" + formatNumber(trend.video_count) + "</div><div class=trend-stat-label>Videos</div></div>";
                html += "</div></div>";
            }
            html += "</div>";
            
            container.innerHTML = html;
        }
        
        function formatNumber(num) {
            if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
            if (num >= 1000) return (num / 1000).toFixed(1) + "K";
            return Math.round(num).toString();
        }
        
        loadTrends();
        setInterval(loadTrends, 30000);
    </script>
</body>
</html>''')
html_content.close()
print("index.html created successfully!")
