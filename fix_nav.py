html_file = open('index.html', 'r', encoding='utf-8')
content = html_file.read()
html_file.close()

# Replace the nav-links div with a scrollable version
old_nav = '<div class="nav-links">'
new_nav = '<div class="nav-links" style="overflow-x:auto;flex-wrap:nowrap;white-space:nowrap;max-width:100%;">'
content = content.replace(old_nav, new_nav)

# Make nav-link not wrap
content = content.replace('.nav-link {', '.nav-link {flex-shrink:0;')

html_file = open('index.html', 'w', encoding='utf-8')
html_file.write(content)
html_file.close()
print("Navigation fixed!")
