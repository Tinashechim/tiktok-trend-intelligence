content = open('index.html', 'r', encoding='utf-8').read()

# Remove Manage nav button
content = content.replace('<button class="nav-link" data-page="manage">Manage</button>', '')

# Remove Manage page div
import re
content = re.sub(r'<div id="manage" class="page">.*?</div>\s*</div>', '', content, flags=re.DOTALL)

# Remove manage from nav click handler
content = content.replace('if (page === "manage") loadManage();', '')

# Remove loadManage and deleteTrend functions
content = re.sub(r'function loadManage\(\) \{.*?\n        \}', '', content, flags=re.DOTALL)
content = re.sub(r'function deleteTrend\(id\) \{.*?\n        \}', '', content, flags=re.DOTALL)

open('index.html', 'w', encoding='utf-8').write(content)
print("Manage tab removed!")
