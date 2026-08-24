with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_relatability = "html += '<p style=\\\"color:#555;\\\">This trend is ' + (relatability > 70 ? 'highly relatable' : relatability > 50 ? 'moderately relatable' : 'not very relatable') + ' to your audience.</p>';"
new_ml = old_relatability + """
            
            // AI Prediction section
            html += '<div style="background:#f8fafc;padding:1rem;border-radius:8px;margin-bottom:1rem;">';
            html += '<h3>🤖 AI Prediction</h3>';
            fetch(API_URL + '/predict/' + trendId)
                .then(function(r){ return r.json(); })
                .then(function(pred){
                    if (pred.prediction !== null) {
                        html += '<p style="color:#555;">Success probability: <strong>' + pred.success_probability + '%</strong></p>';
                    } else {
                        html += '<p style="color:#555;">ML model not loaded</p>';
                    }
                    document.getElementById('analysis-content').insertAdjacentHTML('beforeend', html);
                })
                .catch(function(){});
            """
content = content.replace(old_relatability, new_ml)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

import shutil
shutil.copy('index.html', 'frontend/index.html')
print("ML prediction UI added")
