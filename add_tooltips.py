html_file = open('index.html', 'r', encoding='utf-8')
content = html_file.read()
html_file.close()

# Add tooltip styles before </style>
tooltip_style = '''
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
        [data-tooltip] { cursor: help; }
'''
content = content.replace('</style>', tooltip_style + '</style>')

# Add tooltip attributes to nav links
content = content.replace('data-page="dashboard"', 'data-page="dashboard" data-tooltip="View all current trending content ranked by opportunity score"')
content = content.replace('data-page="analytics"', 'data-page="analytics" data-tooltip="See breakdown of trends by type and score"')
content = content.replace('data-page="calendar"', 'data-page="calendar" data-tooltip="Weekly content plan with recommended posting days"')
content = content.replace('data-page="saved"', 'data-page="saved" data-tooltip="Your bookmarked trends for future reference"')
content = content.replace('data-page="ideas"', 'data-page="ideas" data-tooltip="Generate video content ideas from trending topics"')
content = content.replace('data-page="profile"', 'data-page="profile" data-tooltip="Set your niche and audience size for personalized recommendations"')
content = content.replace('data-page="admin"', 'data-page="admin" data-tooltip="Manually add trends you find on TikTok"')
content = content.replace('data-page="manage"', 'data-page="manage" data-tooltip="Delete outdated or irrelevant trends"')
content = content.replace('onclick="refreshTrends()"', 'onclick="refreshTrends()" data-tooltip="Fetch latest trends from multiple sources automatically"')

# Add tooltip system script before loadTrends()
tooltip_script = '''
        // Tooltip system
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
        
'''
content = content.replace('loadTrends();', tooltip_script + 'loadTrends();')

# Add tooltips to trend metrics in displayTrends
content = content.replace('metric-label>Growth', 'metric-label data-tooltip="Week-over-week growth rate. Higher means the trend is accelerating faster.">Growth')
content = content.replace('metric-label>Competition', 'metric-label data-tooltip="How many creators are using this trend. Lower competition means your content stands out more.">Competition')
content = content.replace('metric-label>Videos', 'metric-label data-tooltip="Total number of videos using this trend.">Videos')

html_file = open('index.html', 'w', encoding='utf-8')
html_file.write(content)
html_file.close()
print("Tooltips added back!")
