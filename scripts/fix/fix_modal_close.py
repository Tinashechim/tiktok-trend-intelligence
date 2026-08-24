import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add class to overlay div and change close button to remove overlay
content = content.replace("modal.style.zIndex = \"9999\";", "modal.style.zIndex = \"9999\";\n            modal.className = \"modal-overlay\";")

# Replace close button onclick
content = content.replace("onclick=\"this.parentElement.remove()\"", "onclick=\"this.closest('.modal-overlay').remove()\"")

# Add overlay click to close (clicking outside content)
overlay_close_script = '''
        document.addEventListener("click", function(e) {
            if (e.target.classList && e.target.classList.contains("modal-overlay")) {
                e.target.remove();
            }
        });
'''
content = content.replace('// initial load', overlay_close_script + '\n        // initial load')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modal close fixed")
