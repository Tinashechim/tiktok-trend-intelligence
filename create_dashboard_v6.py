html_file = open('frontend/index.html', 'w', encoding='utf-8')
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
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        .nav-brand {
            font-size: 1.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            cursor: help;
        }
        .nav-links { display: flex; gap: 0.3rem; flex-wrap: wrap; }
        .nav-link {
            padding: 0.5rem 0.8rem;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 0.85rem;
            color: #666;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .nav-link:hover { background: #f0f0f0; color: #333; }
        .nav-link.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .main-container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        .page { display: none; }
        .page.active { display: block; animation: fadeIn 0.3s; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .page-header { margin-bottom: 2rem; }
        .page-header h1 { font-size: 2rem; color: #333; margin-bottom: 0.5rem; }
        .page-header p { color: #666; }
        
        .filter-bar {
            display: flex;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 0.5rem 1rem;
            border: 1px solid #ddd;
            background: white;
            cursor: pointer;
            border-radius: 20px;
            font-size: 0.9rem;
            transition: all 0.3s;
        }
        .filter-btn:hover { border-color: #667eea; color: #667eea; }
        .filter-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }
        
        .trends-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
        }
        .trend-card {
            background: white;
            border-radius: 12px;
            padding: 1.2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
        }
        .trend-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        .trend-stage {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            margin-bottom: 8px;
            cursor: help;
        }
        .save-btn {
            position: absolute;
            top: 0.8rem;
            right: 0.8rem;
            background: none;
            border: none;
            font-size: 1.1rem;
            cursor: pointer;
            opacity: 0.5;
            transition: opacity 0.3s;
        }
        .save-btn:hover { opacity: 1; }
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
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
            cursor: help;
        }
        .trend-score {
            font-size: 1.3rem;
            font-weight: bold;
            color: #667eea;
            cursor: help;
        }
        .trend-name {
            font-size: 1.1rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }
        .trend-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            background: #f8fafc;
            padding: 10px;
            border-radius: 8px;
        }
        .metric { text-align: center; cursor: help; }
        .metric-value { font-weight: bold; color: #333; font-size: 1rem; }
        .metric-label { font-size: 0.75rem; color: #666; }
        
        .loading { text-align: center; padding: 2rem; color: #666; }
        
        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            animation: slideIn 0.3s;
            z-index: 1000;
        }
        .toast.success { background: #10b981; }
        .toast.error { background: #ef4444; }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .tooltip {
            position: fixed;
            background: #333;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-size: 0.85rem;
            max-width: 250px;
            z-index: 10000;
            pointer-events: none;
            animation: fadeIn 0.2s;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            line-height: 1.4;
        }
        
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .chart-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chart-card h3 { color: #333; margin-bottom: 1rem; cursor: help; }
        .bar-chart {
            display: flex;
            align-items: flex-end;
            gap: 10px;
            height: 200px;
            padding: 10px 0;
        }
        .bar-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100%;
            cursor: help;
        }
        .bar {
            width: 100%;
            max-width: 60px;
            border-radius: 4px 4px 0 0;
            min-height: 4px;
        }
        .bar-label { font-size: 0.7rem; color: #666; margin-top: 5px; }
        .bar-value { font-size: 0.8rem; font-weight: bold; color: #333; margin-bottom: 5px; }
        
        /* Calendar Styles */
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.5rem;
            margin-bottom: 2rem;
        }
        .calendar-day {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            min-height: 150px;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .calendar-day:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        }
        .calendar-day-header {
            font-weight: bold;
            color: #667eea;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }
        .calendar-trend {
            background: #f0f0ff;
            padding: 0.5rem;
            border-radius: 6px;
            margin-bottom: 0.3rem;
            font-size: 0.75rem;
            cursor: help;
        }
        .calendar-trend-name {
            font-weight: bold;
            color: #333;
        }
        .calendar-trend-time {
            color: #666;
            font-size: 0.7rem;
        }
        .calendar-empty {
            color: #ccc;
            text-align: center;
            padding: 1rem;
            font-size: 0.8rem;
        }
        
        .best-times-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .best-times-card h3 { color: #333; margin-bottom: 1rem; }
        .time-slot {
            display: inline-block;
            background: #f0f0ff;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin: 0.25rem;
            font-size: 0.9rem;
            cursor: help;
        }
        
        @media (max-width: 768px) {
            .calendar-grid { grid-template-columns: repeat(2, 1fr); }
            .analytics-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand" data-tooltip="TrendPilot helps you discover trending TikTok content before it goes viral.">TrendPilot</div>
            <div class="nav-links">
                <button class="nav-link active" data-page="dashboard" data-tooltip="See trends that match your niche.">My Opportunities</button>
                <button class="nav-link" data-page="trends" data-tooltip="Browse all detected trends.">All Trends</button>
                <button class="nav-link" data-page="analytics" data-tooltip="Visual charts and insights.">Analytics</button>
                <button class="nav-link" data-page="calendar" data-tooltip="Plan your content for the week.">Calendar</button>
                <button class="nav-link" data-page="saved" data-tooltip="Your bookmarked trends.">Saved</button>
                <button class="nav-link" data-page="ideas" data-tooltip="Generate content ideas.">Content Ideas</button>
                <button class="nav-link" data-page="profile" data-tooltip="Set your preferences.">Profile</button>
            </div>
        </div>
    </nav>
    
    <div class="main-container">
        <div id="dashboard" class="page active">
            <div class="page-header">
                <h1 data-tooltip="Your personalized trend opportunities.">Your Personalized Opportunities</h1>
                <p data-tooltip="Ranked by how well they match your niche.">Set up your profile for recommendations</p>
            </div>
            <div id="dashboard-trends" class="trends-grid">
                <div class="loading">Loading...</div>
            </div>
        </div>
        
        <div id="trends" class="page">
            <div class="page-header">
                <h1>All Active Trends</h1>
                <p>Filter by trend type</p>
            </div>
            <div class="filter-bar">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="sound">Sounds</button>
                <button class="filter-btn" data-filter="hashtag">Hashtags</button>
                <button class="filter-btn" data-filter="topic">Topics</button>
            </div>
            <div id="all-trends" class="trends-grid">
                <div class="loading">Loading...</div>
            </div>
        </div>
        
        <div id="analytics" class="page">
            <div class="page-header">
                <h1>Trend Analytics</h1>
                <p>Visual insights into trends</p>
            </div>
            <div class="analytics-grid">
                <div class="chart-card">
                    <h3 data-tooltip="How trends are distributed by score.">Score Distribution</h3>
                    <div id="score-chart"></div>
                </div>
                <div class="chart-card">
                    <h3 data-tooltip="Breakdown of trend types.">Trend Types</h3>
                    <div id="type-chart"></div>
                </div>
            </div>
            <div class="analytics-grid">
                <div class="chart-card">
                    <h3 data-tooltip="Where trends are in their lifecycle.">Trend Stages</h3>
                    <div id="stage-chart"></div>
                </div>
                <div class="chart-card">
                    <h3 data-tooltip="Fastest growing trends.">Top Growth Trends</h3>
                    <div id="growth-chart"></div>
                </div>
            </div>
        </div>
        
        <div id="calendar" class="page">
            <div class="page-header">
                <h1 data-tooltip="Your weekly content plan based on trending topics.">Content Calendar</h1>
                <p data-tooltip="Plan your posts around the best opportunities.">Schedule your content for maximum reach</p>
            </div>
            
            <div class="best-times-card">
                <h3 data-tooltip="These are the times when TikTok engagement is typically highest.">Best Posting Times</h3>
                <div id="best-times"></div>
                <div id="posting-tips" style="margin-top:1rem;"></div>
            </div>
            
            <h2 style="margin-bottom:1rem;" data-tooltip="Click any day to see suggested content.">Weekly Plan</h2>
            <div id="calendar-grid" class="calendar-grid">
                <div class="loading">Loading calendar...</div>
            </div>
        </div>
        
        <div id="saved" class="page">
            <div class="page-header">
                <h1>Saved Trends</h1>
                <p>Your bookmarked trends</p>
            </div>
            <div id="saved-trends" class="trends-grid">
                <div class="loading">No saved trends yet.</div>
            </div>
        </div>
        
        <div id="ideas" class="page">
            <div class="page-header">
                <h1>Content Ideas Generator</h1>
                <p>Generate video ideas</p>
            </div>
            <div style="background:white;padding:1.5rem;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.1);margin-bottom:2rem;">
                <select id="trend-select" style="width:100%;padding:0.75rem;border:1px solid #ddd;border-radius:8px;margin-bottom:1rem;">
                    <option value="">Select a trend</option>
                </select>
                <button class="btn btn-primary" onclick="generateIdeas()" style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:0.75rem 1.5rem;border:none;border-radius:8px;cursor:pointer;font-weight:bold;">Generate Ideas</button>
            </div>
            <div id="ideas-container"></div>
        </div>
        
        <div id="profile" class="page">
            <div class="page-header">
                <h1>Your Profile</h1>
                <p>Set your preferences</p>
            </div>
            <div style="background:white;padding:2rem;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.1);max-width:600px;">
                <form onsubmit="saveProfile(event)">
                    <div style="margin-bottom:1rem;">
                        <label style="font-weight:bold;">Username</label>
                        <input type="text" id="username" required placeholder="Enter username" style="width:100%;padding:0.75rem;border:1px solid #ddd;border-radius:8px;margin-top:0.5rem;">
                    </div>
                    <div style="margin-bottom:1rem;">
                        <label style="font-weight:bold;">Niche</label>
                        <select id="niche" style="width:100%;padding:0.75rem;border:1px solid #ddd;border-radius:8px;margin-top:0.5rem;">
                            <option value="fitness">Fitness</option>
                            <option value="beauty">Beauty</option>
                            <option value="fashion">Fashion</option>
                            <option value="food">Food</option>
                            <option value="gaming">Gaming</option>
                            <option value="tech">Tech</option>
                            <option value="music">Music</option>
                            <option value="travel">Travel</option>
                            <option value="education">Education</option>
                        </select>
                    </div>
                    <div style="margin-bottom:1rem;">
                        <label style="font-weight:bold;">Followers</label>
                        <input type="number" id="followers" min="0" placeholder="5000" style="width:100%;padding:0.75rem;border:1px solid #ddd;border-radius:8px;margin-top:0.5rem;">
                    </div>
                    <div style="margin-bottom:1rem;">
                        <label style="font-weight:bold;">Engagement Rate (%)</label>
                        <input type="number" id="engagement" min="0" max="100" step="0.1" placeholder="5.0" style="width:100%;padding:0.75rem;border:1px solid #ddd;border-radius:8px;margin-top:0.5rem;">
                    </div>
                    <button type="submit" style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:0.75rem 1.5rem;border:none;border-radius:8px;cursor:pointer;font-weight:bold;">Save Profile</button>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        const API_URL = "http://localhost:8001/api";
        let currentUserId = null;
        let savedTrends = JSON.parse(localStorage.getItem("savedTrends") || "[]");
        let currentFilter = "all";
        
        const tooltip = document.createElement("div");
        tooltip.className = "tooltip";
        tooltip.style.display = "none";
        document.body.appendChild(tooltip);
        
        document.addEventListener("mouseover", function(e) {
            const target = e.target.closest("[data-tooltip]");
            if (target) {
                tooltip.textContent = target.getAttribute("data-tooltip");
                tooltip.style.display = "block";
                const rect = target.getBoundingClientRect();
                const tr = tooltip.getBoundingClientRect();
                let left = rect.left + (rect.width / 2) - (tr.width / 2);
                let top = rect.top - tr.height - 10;
                if (left < 10) left = 10;
                if (left + tr.width > window.innerWidth - 10) left = window.innerWidth - tr.width - 10;
                if (top < 10) top = rect.bottom + 10;
                tooltip.style.left = left + "px";
                tooltip.style.top = top + "px";
            }
        });
        
        document.addEventListener("mouseout", function(e) {
            if (e.target.closest("[data-tooltip]")) tooltip.style.display = "none";
        });
        
        function loadSavedProfile() {
            const savedId = localStorage.getItem("userId");
            const savedProfile = localStorage.getItem("userProfile");
            if (savedId && savedProfile) {
                currentUserId = savedId;
                const profile = JSON.parse(savedProfile);
                document.getElementById("username").value = profile.username;
                document.getElementById("niche").value = profile.niche;
                document.getElementById("followers").value = profile.follower_count;
                document.getElementById("engagement").value = profile.engagement_rate * 100;
            }
        }
        
        document.querySelectorAll(".nav-link").forEach(function(link) {
            link.addEventListener("click", function() {
                var page = this.dataset.page;
                document.querySelectorAll(".nav-link").forEach(function(l) { l.classList.remove("active"); });
                this.classList.add("active");
                document.querySelectorAll(".page").forEach(function(p) { p.classList.remove("active"); });
                document.getElementById(page).classList.add("active");
                if (page === "dashboard") loadDashboard();
                if (page === "trends") loadAllTrends();
                if (page === "analytics") loadAnalytics();
                if (page === "calendar") loadCalendar();
                if (page === "saved") loadSavedTrends();
                if (page === "ideas") loadTrendSelect();
            });
        });
        
        document.querySelectorAll(".filter-btn").forEach(function(btn) {
            btn.addEventListener("click", function() {
                document.querySelectorAll(".filter-btn").forEach(function(b) { b.classList.remove("active"); });
                this.classList.add("active");
                currentFilter = this.dataset.filter;
                loadAllTrends();
            });
        });
        
        async function loadDashboard() {
            const container = document.getElementById("dashboard-trends");
            if (currentUserId) {
                container.innerHTML = "<div class=loading>Loading...</div>";
                try {
                    const response = await fetch(API_URL + "/user/" + currentUserId + "/opportunities");
                    const data = await response.json();
                    if (data.opportunities && data.opportunities.length > 0) {
                        displayTrends(container, data.opportunities, true);
                    } else {
                        container.innerHTML = "<div class=loading>No opportunities found.</div>";
                    }
                } catch (error) {
                    container.innerHTML = "<div class=loading>Error loading</div>";
                }
            } else {
                container.innerHTML = "<div class=loading style=grid-column:1/-1;>Set up your profile to see personalized opportunities.</div>";
            }
        }
        
        async function loadAllTrends() {
            try {
                const response = await fetch(API_URL + "/trends/current");
                const trends = await response.json();
                var filtered = trends;
                if (currentFilter !== "all") filtered = trends.filter(function(t) { return t.type === currentFilter; });
                displayTrends(document.getElementById("all-trends"), filtered, false);
            } catch (error) {
                document.getElementById("all-trends").innerHTML = "<div class=loading>Error loading</div>";
            }
        }
        
        async function loadAnalytics() {
            try {
                const response = await fetch(API_URL + "/analytics/overview");
                const data = await response.json();
                renderScoreChart(data.score_distribution);
                renderTypeChart(data.type_distribution);
                renderStageChart(data.stage_distribution);
                renderGrowthChart(data.growth_data);
            } catch (error) { console.error("Error:", error); }
        }
        
        async function loadCalendar() {
            try {
                const timesResponse = await fetch(API_URL + "/calendar/best-times");
                const timesData = await timesResponse.json();
                
                var timesHtml = "";
                timesData.best_days.forEach(function(day) {
                    timesHtml += "<span class=time-slot data-tooltip='Best day for posting'>" + day + "</span>";
                });
                document.getElementById("best-times").innerHTML = timesHtml;
                
                var tipsHtml = "<ul style=list-style:none;>";
                timesData.tips.forEach(function(tip) {
                    tipsHtml += "<li style=padding:0.25rem 0;color:#666;>• " + tip + "</li>";
                });
                tipsHtml += "</ul>";
                document.getElementById("posting-tips").innerHTML = tipsHtml;
                
                const planResponse = await fetch(API_URL + "/calendar/weekly-plan");
                const planData = await planResponse.json();
                renderCalendar(planData.weekly_plan);
            } catch (error) {
                document.getElementById("calendar-grid").innerHTML = "<div class=loading>Error loading calendar</div>";
            }
        }
        
        function renderCalendar(plan) {
            const container = document.getElementById("calendar-grid");
            
            var html = "";
            plan.forEach(function(day) {
                html += "<div class=calendar-day data-tooltip='Click to see suggestions for " + day.day + "'>";
                html += "<div class=calendar-day-header>" + day.day + "</div>";
                
                if (day.trend_name && day.trend_name !== "Rest day or repost") {
                    html += "<div class=calendar-trend>";
                    html += "<div class=calendar-trend-name>" + day.trend_name + "</div>";
                    html += "<div class=calendar-trend-time>" + day.recommended_time + "</div>";
                    html += "</div>";
                    html += "<div style=font-size:0.7rem;color:#666;margin-top:0.25rem;>" + day.content_suggestion + "</div>";
                } else {
                    html += "<div class=calendar-empty>Rest day</div>";
                }
                
                html += "</div>";
            });
            
            container.innerHTML = html;
        }
        
        function renderScoreChart(distribution) {
            const container = document.getElementById("score-chart");
            const labels = Object.keys(distribution);
            const values = Object.values(distribution);
            const maxValue = Math.max.apply(null, values) || 1;
            var html = "<div class=bar-chart>";
            labels.forEach(function(label, index) {
                var height = (values[index] / maxValue) * 100;
                var color = label === "90-100" ? "#10b981" : label === "80-89" ? "#667eea" : label === "70-79" ? "#f59e0b" : "#ef4444";
                html += "<div class=bar-container data-tooltip='Score range " + label + ": " + values[index] + " trends'>";
                html += "<div class=bar-value>" + values[index] + "</div>";
                html += "<div class=bar style=height:" + height + "%;background:" + color + ";></div>";
                html += "<div class=bar-label>" + label + "</div>";
                html += "</div>";
            });
            html += "</div>";
            container.innerHTML = html;
        }
        
        function renderTypeChart(types) {
            const container = document.getElementById("type-chart");
            const labels = Object.keys(types);
            const values = Object.values(types);
            const maxValue = Math.max.apply(null, values) || 1;
            var html = "<div class=bar-chart>";
            labels.forEach(function(label, index) {
                var height = (values[index] / maxValue) * 100;
                var color = label === "sound" ? "#667eea" : label === "hashtag" ? "#f093fb" : "#4facfe";
                html += "<div class=bar-container data-tooltip='" + label + ": " + values[index] + " trends'>";
                html += "<div class=bar-value>" + values[index] + "</div>";
                html += "<div class=bar style=height:" + height + "%;background:" + color + ";></div>";
                html += "<div class=bar-label>" + label + "</div>";
                html += "</div>";
            });
            html += "</div>";
            container.innerHTML = html;
        }
        
        function renderStageChart(stages) {
            const container = document.getElementById("stage-chart");
            const labels = Object.keys(stages);
            const values = Object.values(stages);
            const maxValue = Math.max.apply(null, values) || 1;
            var html = "<div class=bar-chart>";
            labels.forEach(function(label, index) {
                var height = (values[index] / maxValue) * 100;
                var color = label.indexOf("Early") >= 0 ? "#f59e0b" : label.indexOf("Emerging") >= 0 ? "#ef4444" : label.indexOf("Rising") >= 0 ? "#667eea" : "#10b981";
                var shortLabel = label.replace("🚀 ", "").replace("🔥 ", "").replace("📈 ", "").replace("📉 ", "");
                html += "<div class=bar-container data-tooltip='" + label + ": " + values[index] + " trends'>";
                html += "<div class=bar-value>" + values[index] + "</div>";
                html += "<div class=bar style=height:" + height + "%;background:" + color + ";></div>";
                html += "<div class=bar-label>" + shortLabel + "</div>";
                html += "</div>";
            });
            html += "</div>";
            container.innerHTML = html;
        }
        
        function renderGrowthChart(growthData) {
            const container = document.getElementById("growth-chart");
            if (!growthData.length) { container.innerHTML = "<div class=loading>No data</div>"; return; }
            var html = "<div style=display:flex;flex-direction:column;gap:10px;>";
            growthData.slice(0, 8).forEach(function(item) {
                var width = Math.min((item.growth_rate / 700) * 100, 100);
                var color = item.growth_rate > 300 ? "#ef4444" : item.growth_rate > 100 ? "#f59e0b" : "#667eea";
                html += "<div data-tooltip='" + item.name + " is growing at +" + Math.round(item.growth_rate) + "% per week'>";
                html += "<div style=display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:3px;>";
                html += "<span style=font-weight:bold;>" + item.name + "</span>";
                html += "<span style=color:#666;>+" + Math.round(item.growth_rate) + "%</span>";
                html += "</div>";
                html += "<div style=height:8px;background:#f0f0f0;border-radius:4px;overflow:hidden;>";
                html += "<div style=height:100%;width:" + width + "%;background:" + color + ";border-radius:4px;></div>";
                html += "</div></div>";
            });
            html += "</div>";
            container.innerHTML = html;
        }
        
        function loadSavedTrends() {
            const container = document.getElementById("saved-trends");
            if (savedTrends.length === 0) {
                container.innerHTML = "<div class=loading style=grid-column:1/-1;>No saved trends yet.</div>";
                return;
            }
            container.innerHTML = "<div class=loading>Loading...</div>";
            fetch(API_URL + "/trends/current")
                .then(function(r) { return r.json(); })
                .then(function(trends) {
                    var saved = trends.filter(function(t) { return savedTrends.indexOf(t.id) !== -1; });
                    displayTrends(container, saved, false);
                });
        }
        
        function displayTrends(container, trends, isPersonalized) {
            if (!trends.length) { container.innerHTML = "<div class=loading>No trends found</div>"; return; }
            var html = "";
            trends.forEach(function(trend) {
                var stageStyle = getStageStyle(trend.trend_stage);
                var isSaved = savedTrends.indexOf(trend.id) !== -1;
                var score = isPersonalized ? trend.opportunity_score : trend.trend_score;
                html += "<div class=trend-card>";
                html += "<span class=trend-stage style=" + stageStyle + ">" + trend.trend_stage + "</span>";
                html += "<button class=save-btn onclick=saveTrend(" + trend.id + ")>" + (isSaved ? "🔖" : "📑") + "</button>";
                html += "<div class=trend-header>";
                html += "<span class=trend-type>" + trend.type + "</span>";
                html += "<span class=trend-score>" + Math.round(score) + "/100</span>";
                html += "</div>";
                html += "<div class=trend-name>" + trend.name + "</div>";
                html += "<div class=trend-metrics>";
                html += "<div class=metric><div class=metric-value>" + (trend.growth_rate > 0 ? "+" : "") + Math.round(trend.growth_rate) + "%</div><div class=metric-label>Growth</div></div>";
                html += "<div class=metric><div class=metric-value>" + trend.competition_level + "</div><div class=metric-label>Competition</div></div>";
                html += "<div class=metric><div class=metric-value>" + formatNumber(trend.video_count) + "</div><div class=metric-label>Videos</div></div>";
                html += "</div>";
                if (isPersonalized && trend.compatibility_score) {
                    var compatColor = trend.compatibility_score > 70 ? "#10b981" : trend.compatibility_score > 50 ? "#f59e0b" : "#ef4444";
                    html += "<div style=margin-top:10px;>";
                    html += "<div style=display:flex;justify-content:space-between;font-size:0.85rem;>";
                    html += "<span>Compatibility</span><span style=font-weight:bold;color:" + compatColor + ";>" + Math.round(trend.compatibility_score) + "%</span>";
                    html += "</div>";
                    html += "<div style=height:6px;background:#f0f0f0;border-radius:3px;margin-top:5px;overflow:hidden;>";
                    html += "<div style=height:100%;width:" + trend.compatibility_score + "%;background:" + compatColor + ";border-radius:3px;></div>";
                    html += "</div></div>";
                }
                html += "</div>";
            });
            container.innerHTML = html;
        }
        
        function saveTrend(trendId) {
            var index = savedTrends.indexOf(trendId);
            if (index === -1) { savedTrends.push(trendId); showToast("Trend saved!", "success"); }
            else { savedTrends.splice(index, 1); showToast("Trend removed", "success"); }
            localStorage.setItem("savedTrends", JSON.stringify(savedTrends));
            var activePage = document.querySelector(".page.active").id;
            if (activePage === "dashboard") loadDashboard();
            if (activePage === "trends") loadAllTrends();
            if (activePage === "saved") loadSavedTrends();
        }
        
        async function loadTrendSelect() {
            try {
                const response = await fetch(API_URL + "/trends/current");
                const trends = await response.json();
                var select = document.getElementById("trend-select");
                select.innerHTML = "<option value=>Select a trend</option>";
                trends.forEach(function(trend) {
                    select.innerHTML += "<option value=" + trend.id + ">" + trend.name + " (" + Math.round(trend.trend_score) + ")</option>";
                });
            } catch (error) { console.error("Error:", error); }
        }
        
        async function generateIdeas() {
            var trendId = document.getElementById("trend-select").value;
            if (!trendId) { showToast("Select a trend first", "error"); return; }
            var container = document.getElementById("ideas-container");
            container.innerHTML = "<div class=loading>Generating...</div>";
            try {
                const response = await fetch(API_URL + "/trends/current");
                const trends = await response.json();
                var trend = trends.find(function(t) { return t.id == trendId; });
                if (!trend) { container.innerHTML = "<div class=loading>Not found</div>"; return; }
                var ideas = generateIdeasForTrend(trend);
                container.innerHTML = ideas.map(function(idea) {
                    return "<div style=background:white;border-radius:12px;padding:1.5rem;margin-bottom:1rem;box-shadow:0 2px 10px rgba(0,0,0,0.1);>" +
                        "<h3 style=color:#333;margin-bottom:0.5rem;>" + idea.title + "</h3>" +
                        "<p style=color:#667eea;font-weight:bold;margin-bottom:1rem;>" + idea.hook + "</p>" +
                        "<ul style=list-style:none;margin-bottom:1rem;>" + idea.structure.map(function(s) { return "<li style=padding:0.4rem 0;border-bottom:1px solid #f0f0f0;>" + s + "</li>"; }).join("") + "</ul>" +
                        "<div>" + idea.hashtags.map(function(t) { return "<span style=display:inline-block;background:#f0f0f0;padding:4px 8px;border-radius:4px;margin:2px;font-size:0.85rem;color:#667eea;>#" + t + "</span>"; }).join("") + "</div>" +
                        "<p style=color:#666;margin-top:10px;>Length: " + idea.video_length + "s</p>" +
                        "</div>";
                }).join("");
            } catch (error) { container.innerHTML = "<div class=loading>Error</div>"; }
        }
        
        function generateIdeasForTrend(trend) {
            return [
                {
                    title: "How to use " + trend.name,
                    hook: "You wont believe how " + trend.name + " can transform your videos!",
                    structure: ["Hook with surprising fact", "Show the problem", "Introduce " + trend.name, "Demonstrate", "Share tips", "Call to action"],
                    hashtags: ["fyp", "viral", "trending", "tutorial"],
                    video_length: 30
                },
                {
                    title: "3 secrets about " + trend.name,
                    hook: "Stop scrolling! These secrets will change everything",
                    structure: ["Hook", "Secret 1", "Secret 2", "Secret 3", "Bonus tip", "Question"],
                    hashtags: ["learnontiktok", "tips", "viral"],
                    video_length: 45
                },
                {
                    title: trend.name + " challenge",
                    hook: "I tried " + trend.name + " for 24 hours...",
                    structure: ["Challenge intro", "Attempt 1", "Attempt 2", "Final results", "Challenge viewers"],
                    hashtags: ["challenge", "viral", "fyp"],
                    video_length: 60
                }
            ];
        }
        
        async function saveProfile(event) {
            event.preventDefault();
            var profile = {
                username: document.getElementById("username").value,
                niche: document.getElementById("niche").value,
                follower_count: parseInt(document.getElementById("followers").value || "0"),
                engagement_rate: parseFloat(document.getElementById("engagement").value || "5") / 100,
                goals: ["increase followers"],
                sub_niches: [],
                interests: []
            };
            try {
                const response = await fetch(API_URL + "/user/create", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(profile)
                });
                if (response.ok) {
                    var result = await response.json();
                    localStorage.setItem("userProfile", JSON.stringify(profile));
                    localStorage.setItem("userId", result.id);
                    currentUserId = result.id;
                    showToast("Profile saved!", "success");
                    setTimeout(function() {
                        document.querySelectorAll(".nav-link").forEach(function(l) { l.classList.remove("active"); });
                        document.querySelector("[data-page=dashboard]").classList.add("active");
                        document.querySelectorAll(".page").forEach(function(p) { p.classList.remove("active"); });
                        document.getElementById("dashboard").classList.add("active");
                        loadDashboard();
                    }, 1000);
                }
            } catch (error) { showToast("Error", "error"); }
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
        
        loadSavedProfile();
        loadDashboard();
    </script>
</body>
</html>''')
html_file.close()
print("Calendar dashboard created successfully!")
