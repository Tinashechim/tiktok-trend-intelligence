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
        }
        .nav-brand {
            font-size: 1.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            cursor: help;
        }
        .nav-links { display: flex; gap: 0.5rem; }
        .nav-link {
            padding: 0.5rem 1rem;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 0.9rem;
            color: #666;
            border-radius: 8px;
            transition: all 0.3s;
            position: relative;
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
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            cursor: help;
            position: relative;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.15);
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }
        .stat-label { color: #666; font-size: 0.9rem; margin-top: 0.5rem; }
        
        .trends-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
        }
        .trend-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            position: relative;
            cursor: pointer;
        }
        .trend-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        .trend-stage {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-bottom: 10px;
            cursor: help;
        }
        .save-btn {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            opacity: 0.5;
            transition: opacity 0.3s;
        }
        .save-btn:hover { opacity: 1; }
        .save-btn.saved { opacity: 1; }
        .trend-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .trend-type {
            background: #e0e7ff;
            color: #4f46e5;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            text-transform: uppercase;
            cursor: help;
        }
        .trend-score {
            font-size: 1.5rem;
            font-weight: bold;
            color: #667eea;
            cursor: help;
        }
        .trend-name {
            font-size: 1.2rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
        }
        .trend-metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            background: #f8fafc;
            padding: 15px;
            border-radius: 10px;
        }
        .metric { text-align: center; cursor: help; }
        .metric-value { font-weight: bold; color: #333; font-size: 1.1rem; }
        .metric-label { font-size: 0.8rem; color: #666; }
        
        .saved-badge {
            position: absolute;
            top: 1rem;
            right: 3rem;
            background: #10b981;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            cursor: help;
        }
        
        .profile-form {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 600px;
        }
        .form-group { margin-bottom: 1.5rem; }
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
            color: #333;
        }
        .form-control {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
        }
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        .btn-primary:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(102,126,234,0.4);
        }
        
        .idea-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .idea-title {
            font-size: 1.2rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 0.5rem;
        }
        .idea-hook {
            color: #667eea;
            font-weight: bold;
            margin-bottom: 1rem;
            cursor: help;
        }
        .hashtag {
            display: inline-block;
            padding: 4px 8px;
            background: #f0f0f0;
            border-radius: 4px;
            margin: 2px;
            font-size: 0.9rem;
            color: #667eea;
            cursor: help;
        }
        
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
        .chart-card h3 {
            color: #333;
            margin-bottom: 1rem;
            font-size: 1.1rem;
            cursor: help;
        }
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
            background: linear-gradient(180deg, #667eea, #764ba2);
            border-radius: 4px 4px 0 0;
            transition: height 0.5s;
            min-height: 4px;
        }
        .bar-label {
            font-size: 0.7rem;
            color: #666;
            margin-top: 5px;
            text-align: center;
        }
        .bar-value {
            font-size: 0.8rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }
        
        @media (max-width: 768px) {
            .analytics-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Tooltip Styles */
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
        .tooltip::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 6px solid #333;
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand" data-tooltip="TrendPilot helps you discover trending TikTok content before it goes viral. Click through the tabs to explore opportunities, analytics, and content ideas.">TrendPilot</div>
            <div class="nav-links">
                <button class="nav-link active" data-page="dashboard" data-tooltip="See trends that match your niche and content style. Get personalized opportunity scores for each trend.">My Opportunities</button>
                <button class="nav-link" data-page="trends" data-tooltip="Browse all detected trends. Use filters to see only sounds, hashtags, or topics.">All Trends</button>
                <button class="nav-link" data-page="analytics" data-tooltip="Visual charts showing trend distribution, growth rates, and performance insights.">Analytics</button>
                <button class="nav-link" data-page="saved" data-tooltip="Trends you have bookmarked for future content. Click the bookmark icon on any trend to save it here.">Saved Trends</button>
                <button class="nav-link" data-page="ideas" data-tooltip="Generate video content ideas based on selected trends. Get hooks, structure, and hashtags.">Content Ideas</button>
                <button class="nav-link" data-page="profile" data-tooltip="Set your niche and audience size to get personalized trend recommendations.">Profile</button>
            </div>
        </div>
    </nav>
    
    <div class="main-container">
        <div id="dashboard" class="page active">
            <div class="page-header">
                <h1 id="dashboard-title" data-tooltip="Your personalized trend opportunities based on your profile niche and audience.">Your Personalized Opportunities</h1>
                <p id="dashboard-subtitle" data-tooltip="These trends are ranked by how well they match your content style and audience.">Set up your profile to get personalized recommendations</p>
            </div>
            <div id="dashboard-trends" class="trends-grid">
                <div class="loading">Loading your opportunities...</div>
            </div>
        </div>
        
        <div id="trends" class="page">
            <div class="page-header">
                <h1 data-tooltip="Every trend currently detected on TikTok that is still active and growing.">All Active Trends</h1>
                <p data-tooltip="Use the filter buttons below to narrow down by trend type.">Browse and filter all detected trends</p>
            </div>
            <div class="filter-bar">
                <button class="filter-btn active" data-filter="all" data-tooltip="Show all trend types including sounds, hashtags, and topics.">All</button>
                <button class="filter-btn" data-filter="sound" data-tooltip="Audio clips and music that are trending on TikTok right now.">Sounds</button>
                <button class="filter-btn" data-filter="hashtag" data-tooltip="Popular hashtags that creators are using to get discovered.">Hashtags</button>
                <button class="filter-btn" data-filter="topic" data-tooltip="Content themes and subjects that are gaining traction.">Topics</button>
            </div>
            <div id="all-trends" class="trends-grid">
                <div class="loading">Loading trends...</div>
            </div>
        </div>
        
        <div id="analytics" class="page">
            <div class="page-header">
                <h1 data-tooltip="Charts and visualizations that help you understand trend patterns at a glance.">Trend Analytics</h1>
                <p data-tooltip="Use these insights to make better decisions about which trends to pursue.">Visual insights into trend performance</p>
            </div>
            
            <div class="analytics-grid">
                <div class="chart-card">
                    <h3 data-tooltip="How many trends fall into each score range. Higher scores mean better opportunities.">Score Distribution</h3>
                    <div id="score-chart"></div>
                </div>
                <div class="chart-card">
                    <h3 data-tooltip="The breakdown of trends by type: sounds, hashtags, topics, and formats.">Trend Types</h3>
                    <div id="type-chart"></div>
                </div>
            </div>
            
            <div class="analytics-grid">
                <div class="chart-card">
                    <h3 data-tooltip="Where trends are in their lifecycle. Early and Emerging trends have less competition.">Trend Stages</h3>
                    <div id="stage-chart"></div>
                </div>
                <div class="chart-card">
                    <h3 data-tooltip="The fastest growing trends based on week-over-week growth rate percentage.">Top Growth Trends</h3>
                    <div id="growth-chart"></div>
                </div>
            </div>
        </div>
        
        <div id="saved" class="page">
            <div class="page-header">
                <h1 data-tooltip="Your bookmarked trends. Save trends to build your content pipeline.">Saved Trends</h1>
                <p data-tooltip="Click the bookmark icon on any trend card to add or remove it from this list.">Trends you want to use for future content</p>
            </div>
            <div id="saved-trends" class="trends-grid">
                <div class="loading">No saved trends yet. Click the bookmark icon on any trend to save it.</div>
            </div>
        </div>
        
        <div id="ideas" class="page">
            <div class="page-header">
                <h1 data-tooltip="Get AI-generated video ideas including hooks, structure, and hashtags.">Content Ideas Generator</h1>
                <p data-tooltip="Select a trend and get ready-to-use video concepts.">Generate video ideas based on trending topics</p>
            </div>
            <div class="profile-form" style="margin-bottom: 2rem;">
                <div class="form-group">
                    <label data-tooltip="Choose which trend you want to create content around.">Select a Trend</label>
                    <select id="trend-select" class="form-control">
                        <option value="">Loading trends...</option>
                    </select>
                </div>
                <button class="btn btn-primary" onclick="generateIdeas()" data-tooltip="Generate 3 complete video ideas with hooks, structure, and hashtags.">Generate Ideas</button>
            </div>
            <div id="ideas-container"></div>
        </div>
        
        <div id="profile" class="page">
            <div class="page-header">
                <h1 data-tooltip="Tell us about yourself so we can recommend the best trends for your content.">Your Profile</h1>
                <p data-tooltip="Your niche and audience size help us calculate trend compatibility.">Set your preferences for personalized recommendations</p>
            </div>
            <div class="profile-form">
                <form onsubmit="saveProfile(event)">
                    <div class="form-group">
                        <label data-tooltip="Your TikTok username. This helps identify your account.">Username</label>
                        <input type="text" id="username" class="form-control" required placeholder="Enter username">
                    </div>
                    <div class="form-group">
                        <label data-tooltip="Your main content category. This determines which trends are most relevant to you.">Niche</label>
                        <select id="niche" class="form-control">
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
                    <div class="form-group">
                        <label data-tooltip="How many followers you currently have. This helps estimate potential reach.">Followers</label>
                        <input type="number" id="followers" class="form-control" min="0" placeholder="5000">
                    </div>
                    <div class="form-group">
                        <label data-tooltip="Your average engagement rate (likes + comments + shares divided by views). Typical range is 3-10%.">Engagement Rate (%)</label>
                        <input type="number" id="engagement" class="form-control" min="0" max="100" step="0.1" placeholder="5.0">
                    </div>
                    <button type="submit" class="btn btn-primary" data-tooltip="Save your profile to get personalized trend recommendations.">Save Profile</button>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        const API_URL = "http://localhost:8001/api";
        let currentUserId = null;
        let savedTrends = JSON.parse(localStorage.getItem("savedTrends") || "[]");
        let currentFilter = "all";
        
        // Tooltip System
        const tooltip = document.createElement("div");
        tooltip.className = "tooltip";
        tooltip.style.display = "none";
        document.body.appendChild(tooltip);
        
        document.addEventListener("mouseover", function(e) {
            const target = e.target.closest("[data-tooltip]");
            if (target) {
                const text = target.getAttribute("data-tooltip");
                tooltip.textContent = text;
                tooltip.style.display = "block";
                
                const rect = target.getBoundingClientRect();
                const tooltipRect = tooltip.getBoundingClientRect();
                
                let left = rect.left + (rect.width / 2) - (tooltipRect.width / 2);
                let top = rect.top - tooltipRect.height - 10;
                
                if (left < 10) left = 10;
                if (left + tooltipRect.width > window.innerWidth - 10) {
                    left = window.innerWidth - tooltipRect.width - 10;
                }
                if (top < 10) {
                    top = rect.bottom + 10;
                }
                
                tooltip.style.left = left + "px";
                tooltip.style.top = top + "px";
            }
        });
        
        document.addEventListener("mouseout", function(e) {
            const target = e.target.closest("[data-tooltip]");
            if (target) {
                tooltip.style.display = "none";
            }
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
                
                document.getElementById("dashboard-title").textContent = 
                    "Your " + profile.niche + " Opportunities";
                document.getElementById("dashboard-subtitle").textContent = 
                    "Personalized for @" + profile.username;
            }
        }
        
        document.querySelectorAll(".nav-link").forEach(function(link) {
            link.addEventListener("click", function() {
                var page = this.dataset.page;
                
                document.querySelectorAll(".nav-link").forEach(function(l) {
                    l.classList.remove("active");
                });
                this.classList.add("active");
                
                document.querySelectorAll(".page").forEach(function(p) {
                    p.classList.remove("active");
                });
                document.getElementById(page).classList.add("active");
                
                if (page === "dashboard") loadDashboard();
                if (page === "trends") loadAllTrends();
                if (page === "analytics") loadAnalytics();
                if (page === "saved") loadSavedTrends();
                if (page === "ideas") loadTrendSelect();
            });
        });
        
        document.querySelectorAll(".filter-btn").forEach(function(btn) {
            btn.addEventListener("click", function() {
                document.querySelectorAll(".filter-btn").forEach(function(b) {
                    b.classList.remove("active");
                });
                this.classList.add("active");
                currentFilter = this.dataset.filter;
                loadAllTrends();
            });
        });
        
        async function loadDashboard() {
            const container = document.getElementById("dashboard-trends");
            
            if (currentUserId) {
                container.innerHTML = "<div class=loading>Loading your personalized opportunities...</div>";
                
                try {
                    const response = await fetch(API_URL + "/user/" + currentUserId + "/opportunities");
                    const data = await response.json();
                    
                    if (data.opportunities && data.opportunities.length > 0) {
                        displayTrends(container, data.opportunities, true);
                    } else {
                        container.innerHTML = "<div class=loading>No opportunities found. Try setting up your profile.</div>";
                    }
                } catch (error) {
                    container.innerHTML = "<div class=loading>Error loading opportunities</div>";
                }
            } else {
                container.innerHTML = 
                    "<div class=loading style=grid-column:1/-1;>Set up your profile to see personalized opportunities. " +
                    "Click the Profile tab to get started!</div>";
            }
        }
        
        async function loadAllTrends() {
            try {
                const response = await fetch(API_URL + "/trends/current");
                const trends = await response.json();
                
                var filtered = trends;
                if (currentFilter !== "all") {
                    filtered = trends.filter(function(t) { return t.type === currentFilter; });
                }
                
                displayTrends(document.getElementById("all-trends"), filtered, false);
            } catch (error) {
                document.getElementById("all-trends").innerHTML = 
                    "<div class=loading>Error loading trends</div>";
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
            } catch (error) {
                console.error("Error loading analytics:", error);
            }
        }
        
        function renderScoreChart(distribution) {
            const container = document.getElementById("score-chart");
            const labels = Object.keys(distribution);
            const values = Object.values(distribution);
            const maxValue = Math.max.apply(null, values) || 1;
            
            var html = "<div class=bar-chart>";
            
            labels.forEach(function(label, index) {
                var height = (values[index] / maxValue) * 100;
                var color = "#667eea";
                var tooltipText = "";
                
                if (label === "90-100") {
                    color = "#10b981";
                    tooltipText = "Excellent opportunities. Jump on these trends immediately!";
                } else if (label === "80-89") {
                    color = "#667eea";
                    tooltipText = "Strong opportunities. Worth creating content for.";
                } else if (label === "70-79") {
                    color = "#f59e0b";
                    tooltipText = "Good opportunities. Consider if they match your niche.";
                } else if (label === "60-69") {
                    color = "#f97316";
                    tooltipText = "Moderate opportunities. May have higher competition.";
                } else {
                    color = "#ef4444";
                    tooltipText = "Lower priority. These trends may be saturated or declining.";
                }
                
                html += "<div class=bar-container data-tooltip='" + tooltipText + "'>";
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
                var colors = {
                    "sound": "#667eea",
                    "hashtag": "#f093fb",
                    "topic": "#4facfe",
                    "format": "#10b981"
                };
                var color = colors[label] || "#667eea";
                var tooltipText = "";
                
                if (label === "sound") tooltipText = "Trending audio clips and music. Using trending sounds can boost your video's reach.";
                else if (label === "hashtag") tooltipText = "Popular hashtags that help your content get discovered by new audiences.";
                else if (label === "topic") tooltipText = "Content themes and subjects that are currently popular on the platform.";
                else tooltipText = "Video formats and styles (like before/after, POV, etc.) that are gaining traction.";
                
                html += "<div class=bar-container data-tooltip='" + tooltipText + "'>";
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
                var color = "#667eea";
                var tooltipText = "";
                
                if (label.indexOf("Early") >= 0) {
                    color = "#f59e0b";
                    tooltipText = "Brand new trends with very few videos. High risk but high reward if you jump on early.";
                } else if (label.indexOf("Emerging") >= 0) {
                    color = "#ef4444";
                    tooltipText = "Growing fast with low competition. Best time to create content.";
                } else if (label.indexOf("Rising") >= 0) {
                    color = "#667eea";
                    tooltipText = "Gaining popularity but competition is increasing. Still good opportunities.";
                } else if (label.indexOf("Peak") >= 0) {
                    color = "#10b981";
                    tooltipText = "Very popular but saturated. Harder to stand out.";
                } else {
                    color = "#6b7280";
                    tooltipText = "Past their peak. Generally not worth pursuing.";
                }
                
                var shortLabel = label.replace("🚀 ", "").replace("🔥 ", "").replace("📈 ", "").replace("📉 ", "");
                
                html += "<div class=bar-container data-tooltip='" + tooltipText + "'>";
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
            
            if (!growthData.length) {
                container.innerHTML = "<div class=loading>No data available</div>";
                return;
            }
            
            var html = "<div style=display:flex;flex-direction:column;gap:10px;>";
            
            growthData.slice(0, 8).forEach(function(item) {
                var width = Math.min((item.growth_rate / 700) * 100, 100);
                var color = item.growth_rate > 300 ? "#ef4444" : 
                            item.growth_rate > 100 ? "#f59e0b" : "#667eea";
                var tooltipText = item.name + " is growing at " + Math.round(item.growth_rate) + "% week-over-week. " +
                                  (item.growth_rate > 300 ? "This is an explosive trend!" : 
                                   item.growth_rate > 100 ? "This trend is growing steadily." : 
                                   "This trend is growing moderately.");
                
                html += "<div data-tooltip='" + tooltipText + "'>";
                html += "<div style=display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:3px;>";
                html += "<span style=font-weight:bold;color:#333;>" + item.name + "</span>";
                html += "<span style=color:#666;>+" + Math.round(item.growth_rate) + "%</span>";
                html += "</div>";
                html += "<div style=height:8px;background:#f0f0f0;border-radius:4px;overflow:hidden;>";
                html += "<div style=height:100%;width:" + width + "%;background:" + color + ";border-radius:4px;></div>";
                html += "</div>";
                html += "</div>";
            });
            
            html += "</div>";
            container.innerHTML = html;
        }
        
        function loadSavedTrends() {
            const container = document.getElementById("saved-trends");
            
            if (savedTrends.length === 0) {
                container.innerHTML = 
                    "<div class=loading style=grid-column:1/-1;>No saved trends yet. Click the bookmark icon on any trend to save it.</div>";
                return;
            }
            
            container.innerHTML = "<div class=loading>Loading saved trends...</div>";
            
            fetch(API_URL + "/trends/current")
                .then(function(response) { return response.json(); })
                .then(function(trends) {
                    var saved = trends.filter(function(t) {
                        return savedTrends.indexOf(t.id) !== -1;
                    });
                    
                    if (saved.length === 0) {
                        container.innerHTML = "<div class=loading>No saved trends found</div>";
                    } else {
                        displayTrends(container, saved, false);
                    }
                })
                .catch(function() {
                    container.innerHTML = "<div class=loading>Error loading saved trends</div>";
                });
        }
        
        function displayTrends(container, trends, isPersonalized) {
            if (!trends.length) {
                container.innerHTML = "<div class=loading>No trends found</div>";
                return;
            }
            
            var html = "";
            
            trends.forEach(function(trend) {
                var stageStyle = getStageStyle(trend.trend_stage);
                var isSaved = savedTrends.indexOf(trend.id) !== -1;
                var score = isPersonalized ? trend.opportunity_score : trend.trend_score;
                
                var stageTooltip = "";
                if (trend.trend_stage.indexOf("Early") >= 0) stageTooltip = "Brand new trend with very few videos. Jump on it before it gets crowded!";
                else if (trend.trend_stage.indexOf("Emerging") >= 0) stageTooltip = "Growing fast with low competition. Best time to create content.";
                else if (trend.trend_stage.indexOf("Rising") >= 0) stageTooltip = "Gaining popularity. Still good but competition is increasing.";
                else if (trend.trend_stage.indexOf("Peak") >= 0) stageTooltip = "Very popular but saturated. Harder to stand out now.";
                else stageTooltip = "Past its peak. Generally not worth pursuing.";
                
                html += "<div class=trend-card>";
                html += "<span class=trend-stage style=" + stageStyle + " data-tooltip='" + stageTooltip + "'>" + trend.trend_stage + "</span>";
                
                if (isSaved) {
                    html += "<span class=saved-badge data-tooltip='This trend is in your saved list. Click the bookmark to remove it.'>SAVED</span>";
                }
                
                html += "<button class=save-btn onclick=saveTrend(" + trend.id + ") style=" + (isSaved ? "opacity:1;" : "") + " data-tooltip='" + (isSaved ? "Remove from saved trends" : "Save this trend for later") + "'>" + (isSaved ? "🔖" : "📑") + "</button>";
                html += "<div class=trend-header>";
                html += "<span class=trend-type data-tooltip='" + getTypeTooltip(trend.type) + "'>" + trend.type + "</span>";
                html += "<span class=trend-score data-tooltip='Trend score out of 100. Higher = better opportunity. Calculated from growth rate, engagement, and competition.'>" + Math.round(score) + "/100</span>";
                html += "</div>";
                html += "<div class=trend-name>" + trend.name + "</div>";
                html += "<div class=trend-metrics>";
                html += "<div class=metric data-tooltip='Week-over-week growth rate. Higher percentage means the trend is accelerating faster.'><div class=metric-value>" + (trend.growth_rate > 0 ? "+" : "") + Math.round(trend.growth_rate) + "%</div><div class=metric-label>Growth</div></div>";
                html += "<div class=metric data-tooltip='How many other creators are already using this trend. Lower competition means your content is more likely to stand out.'><div class=metric-value>" + trend.competition_level + "</div><div class=metric-label>Competition</div></div>";
                html += "<div class=metric data-tooltip='Total number of videos using this trend. More videos usually means more saturated.'><div class=metric-value>" + formatNumber(trend.video_count) + "</div><div class=metric-label>Videos</div></div>";
                html += "</div>";
                
                if (isPersonalized && trend.compatibility_score) {
                    var compatColor = trend.compatibility_score > 70 ? "#10b981" : 
                                      trend.compatibility_score > 50 ? "#f59e0b" : "#ef4444";
                    html += "<div style=margin-top:15px; data-tooltip='How well this trend matches your niche and content style. Higher compatibility means your audience is more likely to engage.'>";
                    html += "<div style=display:flex;justify-content:space-between;font-size:0.9rem;>";
                    html += "<span>Compatibility</span>";
                    html += "<span style=font-weight:bold;color:" + compatColor + ";>" + Math.round(trend.compatibility_score) + "%</span>";
                    html += "</div>";
                    html += "<div style=height:6px;background:#f0f0f0;border-radius:3px;margin-top:5px;overflow:hidden;>";
                    html += "<div style=height:100%;width:" + trend.compatibility_score + "%;background:" + compatColor + ";border-radius:3px;></div>";
                    html += "</div></div>";
                }
                
                html += "</div>";
            });
            
            container.innerHTML = html;
        }
        
        function getTypeTooltip(type) {
            if (type === "sound") return "Trending audio clip or music. Using trending sounds can significantly boost your video's reach because TikTok's algorithm favors videos with popular audio.";
            if (type === "hashtag") return "Popular hashtag. Including trending hashtags helps your content get discovered by users browsing that hashtag.";
            if (type === "topic") return "Content theme or subject that is currently popular. Creating content around trending topics can help you reach a wider audience.";
            if (type === "format") return "Video style or structure (like before/after, POV, etc.) that is gaining popularity. Using trending formats can increase engagement.";
            return "Trend type";
        }
        
        function saveTrend(trendId) {
            var index = savedTrends.indexOf(trendId);
            
            if (index === -1) {
                savedTrends.push(trendId);
                showToast("Trend saved!", "success");
            } else {
                savedTrends.splice(index, 1);
                showToast("Trend removed", "success");
            }
            
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
                    select.innerHTML += "<option value=" + trend.id + ">" + trend.name + " (Score: " + Math.round(trend.trend_score) + ")</option>";
                });
            } catch (error) {
                console.error("Error loading trends:", error);
            }
        }
        
        async function generateIdeas() {
            var trendId = document.getElementById("trend-select").value;
            
            if (!trendId) {
                showToast("Please select a trend first", "error");
                return;
            }
            
            var container = document.getElementById("ideas-container");
            container.innerHTML = "<div class=loading>Generating ideas...</div>";
            
            try {
                const response = await fetch(API_URL + "/trends/current");
                const trends = await response.json();
                
                var trend = trends.find(function(t) { return t.id == trendId; });
                
                if (!trend) {
                    container.innerHTML = "<div class=loading>Trend not found</div>";
                    return;
                }
                
                var ideas = generateIdeasForTrend(trend);
                
                container.innerHTML = ideas.map(function(idea) {
                    return "<div class=idea-card>" +
                        "<div class=idea-title>" + idea.title + "</div>" +
                        "<div class=idea-hook data-tooltip='The opening line of your video. The first 3 seconds are critical for stopping viewers from scrolling.'>" + idea.hook + "</div>" +
                        "<ul style=list-style:none;margin-bottom:1rem;>" + idea.structure.map(function(step) {
                            return "<li style=padding:0.5rem 0;border-bottom:1px solid #f0f0f0;>" + step + "</li>";
                        }).join("") + "</ul>" +
                        "<div>" + idea.hashtags.map(function(tag) {
                            return "<span class=hashtag data-tooltip='Using relevant hashtags helps your video get discovered by users searching for that topic.'>#" + tag + "</span>";
                        }).join("") + "</div>" +
                        "<p style=color:#666;margin-top:10px; data-tooltip='Recommended video length. Shorter videos (15-30 sec) often perform better for quick tips, while longer videos (45-60 sec) work for tutorials and challenges.'>Video Length: " + idea.video_length + " seconds</p>" +
                        "</div>";
                }).join("");
                
            } catch (error) {
                container.innerHTML = "<div class=loading>Error generating ideas</div>";
            }
        }
        
        function generateIdeasForTrend(trend) {
            var ideas = [];
            
            ideas.push({
                title: "How to use " + trend.name + " in your content",
                hook: "You wont believe how " + trend.name + " can transform your videos!",
                structure: [
                    "Hook with surprising fact about " + trend.name,
                    "Show the problem your audience faces",
                    "Introduce " + trend.name + " as the solution",
                    "Demonstrate with real examples",
                    "Share 3 pro tips for best results",
                    "Call to action: Follow for more!"
                ],
                hashtags: ["fyp", "viral", "trending", "tutorial", "howto"],
                video_length: 30
            });
            
            ideas.push({
                title: "3 secrets about " + trend.name + " nobody tells you",
                hook: "Stop scrolling! These " + trend.name + " secrets will change everything",
                structure: [
                    "Hook: I discovered something crazy...",
                    "Secret 1 with visual demonstration",
                    "Secret 2 with before/after",
                    "Secret 3 that surprises viewers",
                    "Bonus tip for engagement",
                    "Question to drive comments"
                ],
                hashtags: ["learnontiktok", "tips", "howto", "viral", "secrets"],
                video_length: 45
            });
            
            ideas.push({
                title: trend.name + " challenge - Can you do it?",
                hook: "I tried " + trend.name + " for 24 hours and this happened...",
                structure: [
                    "Challenge introduction with stakes",
                    "Attempt 1 - The struggle",
                    "Attempt 2 - Getting better",
                    "Final attempt - Success!",
                    "Reveal results and lessons",
                    "Challenge viewers to try"
                ],
                hashtags: ["challenge", "viral", "fyp", "trending", "trythis"],
                video_length: 60
            });
            
            return ideas;
        }
        
        async function saveProfile(event) {
            event.preventDefault();
            
            var profile = {
                username: document.getElementById("username").value,
                niche: document.getElementById("niche").value,
                follower_count: parseInt(document.getElementById("followers").value || "0"),
                engagement_rate: parseFloat(document.getElementById("engagement").value || "5") / 100,
                goals: ["increase followers", "boost engagement"],
                sub_niches: [],
                interests: []
            };
            
            try {
                const response = await fetch(API_URL + "/user/create", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(profile)
                });
                
                if (response.ok) {
                    var result = await response.json();
                    localStorage.setItem("userProfile", JSON.stringify(profile));
                    localStorage.setItem("userId", result.id);
                    currentUserId = result.id;
                    
                    showToast("Profile saved! Loading your opportunities...", "success");
                    
                    document.getElementById("dashboard-title").textContent = 
                        "Your " + profile.niche + " Opportunities";
                    document.getElementById("dashboard-subtitle").textContent = 
                        "Personalized for @" + profile.username;
                    
                    setTimeout(function() {
                        document.querySelectorAll(".nav-link").forEach(function(l) {
                            l.classList.remove("active");
                        });
                        document.querySelector("[data-page=dashboard]").classList.add("active");
                        document.querySelectorAll(".page").forEach(function(p) {
                            p.classList.remove("active");
                        });
                        document.getElementById("dashboard").classList.add("active");
                        loadDashboard();
                    }, 1000);
                } else {
                    showToast("Error saving profile", "error");
                }
            } catch (error) {
                showToast("Error connecting to server", "error");
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
            
            setTimeout(function() {
                toast.remove();
            }, 3000);
        }
        
        loadSavedProfile();
        loadDashboard();
    </script>
</body>
</html>''')
html_file.close()
print("Dashboard with tooltips created successfully!")
