html_file = open('frontend/index.html', 'r', encoding='utf-8')
content = html_file.read()
html_file.close()

content = content.replace('http://localhost:8001/api', 'https://tiktok-trend-intelligence.onrender.com/api')

html_file = open('frontend/index.html', 'w', encoding='utf-8')
html_file.write(content)
html_file.close()

print("Frontend updated to use live API!")
