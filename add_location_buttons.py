import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the local trends innerHTML line and add buttons
old_local = "localC.innerHTML += '<div class=\"trend-card\"><strong>' + t.name + '</strong><br><span style=\"font-size:0.85rem;color:#666;\">Score: ' + Math.round(t.trend_score) + ' | Growth: +' + Math.round(t.growth_rate) + '%</span><br><span style=\"font-size:0.8rem;color:#10b981;\">Top: ' + t.top_locations.slice(0,3).join(', ') + '</span></div>';"

new_local = '''localC.innerHTML += '<div class="trend-card"><strong>' + t.name + '</strong><br><span style="font-size:0.85rem;color:#666;">Score: ' + Math.round(t.trend_score) + ' | Growth: +' + Math.round(t.growth_rate) + '%</span><br><span style="font-size:0.8rem;color:#10b981;">Top: ' + t.top_locations.slice(0,3).join(', ') + '</span><br>' +
                '<button onclick="toggleSave(' + t.id + ')" style="margin-top:8px;background:none;border:none;cursor:pointer;">' + (savedTrends.indexOf(t.id)>-1 ? 'Remove' : 'Save') + '</button>' +
                '<button onclick="showAnalysis(' + t.id + ')" style="margin-top:8px;background:#667eea;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;margin-left:5px;">Analysis</button></div>';'''

if old_local in content:
    content = content.replace(old_local, new_local)
    print("Local trend buttons added")
else:
    print("Local trend line not found, trying regex")
    pattern = re.compile(r"localC\.innerHTML \+= '.*?';", re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(new_local, content)
        print("Local trend buttons added via regex")
    else:
        print("Could not find local trend line")

# Do the same for international
old_intl = "intlC.innerHTML += '<div class=\"trend-card\"><strong>' + t.name + '</strong><br><span style=\"font-size:0.85rem;color:#666;\">Score: ' + Math.round(t.trend_score) + ' | Growth: +' + Math.round(t.growth_rate) + '%</span><br><span style=\"font-size:0.8rem;color:#10b981;\">Top: ' + t.top_locations.slice(0,3).join(', ') + '</span></div>';"

new_intl = '''intlC.innerHTML += '<div class="trend-card"><strong>' + t.name + '</strong><br><span style="font-size:0.85rem;color:#666;">Score: ' + Math.round(t.trend_score) + ' | Growth: +' + Math.round(t.growth_rate) + '%</span><br><span style="font-size:0.8rem;color:#10b981;">Top: ' + t.top_locations.slice(0,3).join(', ') + '</span><br>' +
                '<button onclick="toggleSave(' + t.id + ')" style="margin-top:8px;background:none;border:none;cursor:pointer;">' + (savedTrends.indexOf(t.id)>-1 ? 'Remove' : 'Save') + '</button>' +
                '<button onclick="showAnalysis(' + t.id + ')" style="margin-top:8px;background:#667eea;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;margin-left:5px;">Analysis</button></div>';'''

if old_intl in content:
    content = content.replace(old_intl, new_intl)
    print("International trend buttons added")
else:
    print("International trend line not found, trying regex")
    pattern = re.compile(r"intlC\.innerHTML \+= '.*?';", re.DOTALL)
    if pattern.search(content):
        content = pattern.sub(new_intl, content)
        print("International trend buttons added via regex")
    else:
        print("Could not find international trend line")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Copy to frontend
import shutil
shutil.copy('index.html', 'frontend/index.html')
print("Done")
