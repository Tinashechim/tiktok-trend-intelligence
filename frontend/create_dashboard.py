html_file = open('index.html', 'w', encoding='utf-8')
html_file.write('''<!DOCTYPE html>
<html>
<head>
    <title>TikTok Trend Intelligence</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: "Segoe UI", Arial, sans-serif;
            background: #f5f7fa;
            min-height: 100vh;
        }
        
        /* Navigation */
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
        }
        .nav-links {
            display: flex;
            gap: 1rem;
        }
        .nav-link {
            padding: 0.5rem 1rem;
            border: none;
            background: none;
            cursor: pointer;
            font-size: 1rem;
            color: #666;
            border-radius: 8px;
            transition: all 0.3s;
        }
        .nav-link:hover {
            background: #f0f0f0;
            color: #333;
        }
        .nav-link.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        /* Main Container */
        .main-container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        /* Pages */
        .page { display: none; }
        .page.active { display: block; animation: fadeIn 0.3s; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Header */
        .page-header {
            margin-bottom: 2rem;
        }
        .page-header h1 {
            font-size: 2rem;
            color: #333;
            margin-bottom: 0.5rem;
        }
        .page-header p {
            color: #666;
        }
        
        /* Stats */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        .stat-icon {
            width: 50px;
            height: 50px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            color: white;
        }
        .stat-info {
            display: flex;
            flex-direction: column;
        }
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #333;
        }
        .stat-label {
            color: #666;
            font-size: 0.9rem;
        }
        
        /* Trend Cards */
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
            overflow: hidden;
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
        }
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
        }
        .trend-score {
            font-size: 1.5rem;
            font-weight: bold;
            color: #667eea;
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
        .metric {
            text-align: center;
        }
        .metric-value {
            font-weight: bold;
            color: #333;
            font-size: 1.1rem;
        }
        .metric-label {
            font-size: 0.8rem;
            color: #666;
        }
        
        /* Profile Form */
        .profile-form {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 600px;
        }
        .form-group {
            margin-bottom: 1.5rem;
        }
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
        .form-control:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
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
        
        /* Content Ideas */
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
        }
        .idea-structure {
            list-style: none;
            margin-bottom: 1rem;
        }
        .idea-structure li {
            padding: 0.5rem 0;
            border-bottom: 1px solid #f0f0f0;
        }
        .idea-structure li:last-child {
            border-bottom: none;
        }
        .hashtag {
            display: inline-block;
            padding: 4px 8px;
            background: #f0f0f0;
            border-radius: 4px;
            margin: 2px;
            font-size: 0.9rem;
            color: #667eea;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
            color: #666;
        }
        
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
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand">TrendPilot</div>
            <div class="nav-links">
                <button class="nav-link active" data-page="dashboard">Dashboard</button>
                <button class="nav-link" data-page="trends">All Trends</button>
                <button class="nav-link" data-page="ideas">Content Ideas</button>
                <button class="nav-link" data-page="profile">Profile</button>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div class="main-container">
        <!-- Dashboard Page -->
        <div id="dashboard" class="page active">
            <div class="page-header">
                <h1>Todays Opportunities</h1>
                <p>Top trends you should consider for your content</p>
            </div>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon" style="background: linear-gradient(135deg, #667eea, #764ba2);">T</div>
                    <div class="stat-info">
                        <div class="stat-value" id="total-trends">0</div>
                        <div class="stat-label">Active Trends</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb, #f5576c);">S</div>
                    <div class="stat-info">
                        <div class="stat-value" id="top-score">0</div>
                        <div class="stat-label">Top Score</div>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe, #00f2fe);">G</div>
                    <div class="stat-info">
                        <div class="stat-value" id="avg-growth">0%</div>
                        <div class="stat-label">Avg Growth</div>
                    </div>
                </div>
            </div>
            
            <div id="dashboard-trends" class="trends-grid">
                <div class="loading">Loading trends...</div>
            </div>
        </div>
        
        <!-- All Trends Page -->
        <div id="trends" class="page">
            <div class="page-header">
                <h1>All Trends</h1>
                <p>Browse all detected trends</p>
            </div>
            <div id="all-trends" class="trends-grid">
                <div class="loading">Loading trends...</div>
            </div>
        </div>
        
        <!-- Content Ideas Page -->
        <div id="ideas" class="page">
            <div class="page-header">
                <h1>Content Ideas Generator</h1>
                <p>Generate video ideas based on trending topics</p>
            </div>
            
            <div class="profile-form" style="margin-bottom: 2rem;">
                <div class="form-group">
                    <label>Select a Trend</label>
                    <select id="trend-select" class="form-control">
                        <option value="">Loading trends...</option>
                    </select>
                </div>
                <button class="btn btn-primary" onclick="generateIdeas()">Generate Ideas</button>
            </div>
            
            <div id="ideas-container"></div>
        </div>
        
        <!-- Profile Page -->
        <div id="profile" class="page">
            <div class="page-header">
                <h1>Your Profile</h1>
                <p>Set your preferences for personalized recommendations</p>
            </div>
            
            <div class="profile-form">
                <form onsubmit="saveProfile(event)">
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" id="username" class="form-control" required placeholder="Enter username">
                    </div>
                    
                    <div class="form-group">
                        <label>Niche</label>
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
                        <label>Followers</label>
                        <input type="number" id="followers" class="form-control" min="0" placeholder="5000">
                    </div>
                    
                    <div class="form-group">
                        <label>Engagement Rate (%)</label>
                        <input type="number" id="engagement" class="form-control" min="0" max="100" step="0.1" placeholder="5.0">
                    </div>
                    
                    <button type="submit" class="btn btn-primary">Save Profile</button>
                </form>
            </div>
        </div>
    </div>
    
    <script>
        const API_URL = "http://localhost:8001/api";
        
        // Navigation
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
                if (page === "ideas") loadTrendSelect();
            });
        });
        
        // Load Dashboard
        async function loadDashboard() {
            try {
                const response = await fetch(API_URL + "/trends/current");
                const trends = await response.json();
                
                updateStats(trends);
                displayTrends("dashboard-trends", trends.slice(0, 6));
            } catch (error) {
                document.getElementById("dashboard-trends").innerHTML = 
                    "<div class=loading>Error loading trends</div>";
            }
        }
        
        // Load All Trends
        async function loadAllTrends() {
            try {
                const response = await fetch(API_URL + "/trends/current");
                const trends = await response.json();
                
                displayTrends("all-trends", trends);
            } catch (error) {
                document.getElementById("all-trends").innerHTML = 
                    "<div class=loading>Error loading trends</div>";
            }
        }
        
        // Load Trend Select
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
        
        // Update Stats
        function updateStats(trends) {
            if (!trends.length) return;
            
            document.getElementById("total-trends").textContent = trends.length;
            
            var topScore = 0;
            var totalGrowth = 0;
            
            trends.forEach(function(trend) {
                if (trend.trend_score > topScore) topScore = trend.trend_score;
                totalGrowth += trend.growth_rate;
            });
            
            document.getElementById("top-score").textContent = Math.round(topScore);
            document.getElementById("avg-growth").textContent = Math.round(totalGrowth / trends.length) + "%";
        }
        
        // Display Trends
        function displayTrends(containerId, trends) {
            var container = document.getElementById(containerId);
            
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
                html += "</div>";
                html += "</div>";
            });
            
            container.innerHTML = html;
        }
        
        // Get Stage Style
        function getStageStyle(stage) {
            if (stage.indexOf("Early") >= 0) return "background:#fef3c7;color:#d97706;";
            if (stage.indexOf("Emerging") >= 0) return "background:#fee2e2;color:#dc2626;";
            if (stage.indexOf("Rising") >= 0) return "background:#e0e7ff;color:#4f46e5;";
            if (stage.indexOf("Peak") >= 0) return "background:#d1fae5;color:#059669;";
            return "background:#f3f4f6;color:#6b7280;";
        }
        
        // Generate Ideas
        async function generateIdeas() {
            var trendId = document.getElementById("trend-select").value;
            
            if (!trendId) {
                showToast("Please select a trend first", "error");
                return;
            }
            
            var container = document.getElementById("ideas-container");
            container.innerHTML = "<div class=loading>Generating ideas...</div>";
            
            // Get trend details
            try {
                const response = await fetch(API_URL + "/trends/current");
                const trends = await response.json();
                
                var trend = trends.find(function(t) { return t.id == trendId; });
                
                if (!trend) {
                    container.innerHTML = "<div class=loading>Trend not found</div>";
                    return;
                }
                
                // Generate ideas based on trend
                var ideas = generateIdeasForTrend(trend);
                
                container.innerHTML = ideas.map(function(idea) {
                    return "<div class=idea-card>" +
                        "<div class=idea-title>" + idea.title + "</div>" +
                        "<div class=idea-hook>" + idea.hook + "</div>" +
                        "<ul class=idea-structure>" + idea.structure.map(function(step) {
                            return "<li>" + step + "</li>";
                        }).join("") + "</ul>" +
                        "<div>" + idea.hashtags.map(function(tag) {
                            return "<span class=hashtag>#" + tag + "</span>";
                        }).join("") + "</div>" +
                        "<p style=color:#666;margin-top:10px;>Video Length: " + idea.video_length + " seconds</p>" +
                        "</div>";
                }).join("");
                
            } catch (error) {
                container.innerHTML = "<div class=loading>Error generating ideas</div>";
            }
        }
        
        // Generate Ideas for Trend
        function generateIdeasForTrend(trend) {
            var ideas = [];
            
            ideas.push({
                title: "How to use " + trend.name + " in your content",
                hook: "You wont believe how " + trend.name + " can transform your videos!",
                structure: [
                    "Hook with surprising fact",
                    "Introduce " + trend.name,
                    "Show the transformation",
                    "Share 3 pro tips",
                    "Call to action"
                ],
                hashtags: ["fyp", "viral", "trending", "tutorial"],
                video_length: 30
            });
            
            ideas.push({
                title: "3 secrets about " + trend.name + " nobody tells you",
                hook: "Stop scrolling! These " + trend.name + " secrets will change everything",
                structure: [
                    "Hook with secret reveal",
                    "Secret 1 about " + trend.name,
                    "Secret 2 about " + trend.name,
                    "Secret 3 about " + trend.name,
                    "Engagement question"
                ],
                hashtags: ["learnontiktok", "tips", "howto", "viral"],
                video_length: 45
            });
            
            ideas.push({
                title: trend.name + " challenge - 24 hour edition",
                hook: "I tried " + trend.name + " for 24 hours and this happened...",
                structure: [
                    "Challenge introduction",
                    "Attempt 1 with " + trend.name,
                    "Attempt 2 with " + trend.name,
                    "Final results",
                    "Encourage viewers to try"
                ],
                hashtags: ["challenge", "viral", "fyp", "trending"],
                video_length: 60
            });
            
            return ideas;
        }
        
        // Save Profile
        async function saveProfile(event) {
            event.preventDefault();
            
            var profile = {
                username: document.getElementById("username").value,
                niche: document.getElementById("niche").value,
                follower_count: parseInt(document.getElementById("followers").value || "0"),
                engagement_rate: parseFloat(document.getElementById("engagement").value || "5") / 100,
                goals: ["increase followers", "boost engagement"]
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
                    showToast("Profile saved successfully!", "success");
                    
                    // Switch to dashboard
                    document.querySelectorAll(".nav-link").forEach(function(l) {
                        l.classList.remove("active");
                    });
                    document.querySelector("[data-page=dashboard]").classList.add("active");
                    document.querySelectorAll(".page").forEach(function(p) {
                        p.classList.remove("active");
                    });
                    document.getElementById("dashboard").classList.add("active");
                    loadDashboard();
                } else {
                    showToast("Error saving profile", "error");
                }
            } catch (error) {
                showToast("Error connecting to server", "error");
            }
        }
        
        // Format Number
        function formatNumber(num) {
            if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
            if (num >= 1000) return (num / 1000).toFixed(1) + "K";
            return Math.round(num).toString();
        }
        
        // Show Toast
        function showToast(message, type) {
            var toast = document.createElement("div");
            toast.className = "toast " + type;
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(function() {
                toast.remove();
            }, 3000);
        }
        
        // Load on start
        loadDashboard();
    </script>
</body>
</html>''')
html_file.close()
print("Complete dashboard created successfully!")
