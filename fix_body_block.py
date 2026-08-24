import re

with open('deploy_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern matches the broken body assignment and the following for loop
pattern = r'body = "Top trends right now:.*?(?=for email, settings)'
replacement = '''body = "Top trends right now:\\n\\n"
            for t in top_trends:
                body += f"{t.trend_name} - Score: {t.trend_score}\\n"
                body += f"Growth: +{t.growth_rate}% | Competition: {t.competition_level}\\n\\n"
            '''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed alert_loop body block")
