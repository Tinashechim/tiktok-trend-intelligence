content = open('index.html', 'r', encoding='utf-8').read()

# Add tooltip CSS before </style>
tooltip_css = '''
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
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            line-height: 1.4;
            display: none;
        }
        [data-tooltip] { cursor: help; }
'''
content = content.replace('</style>', tooltip_css + '</style>')

# Add tooltip attributes to nav buttons
content = content.replace('data-page="dashboard"', 'data-page="dashboard" data-tooltip="View all current trending content ranked by opportunity score"')
content = content.replace('data-page="analytics"', 'data-page="analytics" data-tooltip="See breakdown of trends by type, score, and growth"')
content = content.replace('data-page="calendar"', 'data-page="calendar" data-tooltip="Weekly content plan with recommended posting days"')
content = content.replace('data-page="saved"', 'data-page="saved" data-tooltip="Your bookmarked trends for future reference"')
content = content.replace('data-page="ideas"', 'data-page="ideas" data-tooltip="Generate video content ideas from trending topics"')
content = content.replace('data-page="profile"', 'data-page="profile" data-tooltip="Set your niche for personalized recommendations"')
content = content.replace('data-page="admin"', 'data-page="admin" data-tooltip="Manually add trends you find on TikTok"')
content = content.replace('onclick="refreshTrends()"', 'onclick="refreshTrends()" data-tooltip="Fetch latest trends from multiple sources"')

# Add tooltip system script before loadTrends()
tooltip_script = '''
        // Tooltip System
        var tooltip = document.createElement("div");
        tooltip.className = "tooltip";
        document.body.appendChild(tooltip);
        
        document.addEventListener("mouseover", function(e) {
            var target = e.target.closest("[data-tooltip]");
            if (target) {
                tooltip.textContent = target.getAttribute("data-tooltip");
                tooltip.style.display = "block";
                var rect = target.getBoundingClientRect();
                var tr = tooltip.getBoundingClientRect();
                var left = rect.left + (rect.width / 2) - (tr.width / 2);
                var top = rect.top - tr.height - 10;
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
        
'''
content = content.replace('loadTrends();', tooltip_script + 'loadTrends();', 1)

open('index.html', 'w', encoding='utf-8').write(content)
print("Tooltips added!")
