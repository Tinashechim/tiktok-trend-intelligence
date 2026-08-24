import re
with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'body = "Top trends right now:.*?for email, settings', re.DOTALL)
replacement = '''body = "Top trends right now:\\n\\n"
            for t in top_trends:
                body += f"{t.trend_name} - Score: {t.trend_score}\\n"
                body += f"Growth: +{t.growth_rate}% | Competition: {t.competition_level}\\n\\n"
            for email, settings'''

new_content = pattern.sub(replacement, content)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Exact fix applied")
