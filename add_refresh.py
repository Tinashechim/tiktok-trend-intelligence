html_file = open('index.html', 'r', encoding='utf-8')
content = html_file.read()
html_file.close()

# Add refresh button to navbar
content = content.replace('</nav>', '<button class="nav-link" onclick="refreshTrends()" style="background:#10b981;color:white;">🔄 Refresh Trends</button></nav>')

# Add refreshTrends function before closing script
refresh_function = '''
        async function refreshTrends() {
            showToast("Fetching latest trends...", "success");
            try {
                const response = await fetch(API_URL + "/refresh", { method: "POST" });
                const data = await response.json();
                showToast("Updated " + data.count + " trends!", "success");
                loadTrends();
            } catch (error) {
                showToast("Error refreshing trends", "error");
            }
        }
'''
content = content.replace('</script>', refresh_function + '</script>')

html_file = open('index.html', 'w', encoding='utf-8')
html_file.write(content)
html_file.close()
print("Frontend updated with refresh button!")
