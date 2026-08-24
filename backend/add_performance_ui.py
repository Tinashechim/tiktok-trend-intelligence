with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert performance prediction after AI Prediction section
old_ai_prediction = "fetch(API_URL + '/predict/' + trendId)"
new_performance_block = """fetch(API_URL + '/predict/' + trendId)"""
# We need to add a second fetch after the first one. Easier to insert after the AI Prediction block closes.
# Find the line where we set analysis-content innerHTML after AI Prediction.
old_line = "document.getElementById('analysis-content').insertAdjacentHTML('beforeend', html);"
new_line = """document.getElementById('analysis-content').insertAdjacentHTML('beforeend', html);
            
            // Performance prediction
            var authUser = localStorage.getItem('authUser');
            if (authUser) {
                var user = JSON.parse(authUser);
                fetch(API_URL + '/predict-performance', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({trend_id: trendId, user_id: user.id})
                })
                .then(function(r){ return r.json(); })
                .then(function(perf){
                    if (perf.predicted_views) {
                        var perfHtml = '<div style="background:#f0fdf4;padding:1rem;border-radius:8px;margin-bottom:1rem;">';
                        perfHtml += '<h3>📈 ML Performance Forecast</h3>';
                        perfHtml += '<p>Views: <strong>' + formatNumber(perf.predicted_views) + '</strong></p>';
                        perfHtml += '<p>Likes: <strong>' + formatNumber(perf.predicted_likes) + '</strong></p>';
                        perfHtml += '<p>Comments: <strong>' + formatNumber(perf.predicted_comments) + '</strong></p>';
                        perfHtml += '<p>Shares: <strong>' + formatNumber(perf.predicted_shares) + '</strong></p>';
                        perfHtml += '</div>';
                        document.getElementById('analysis-content').insertAdjacentHTML('beforeend', perfHtml);
                    }
                })
                .catch(function(){});
            }"""
content = content.replace(old_line, new_line)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Performance prediction UI added")
