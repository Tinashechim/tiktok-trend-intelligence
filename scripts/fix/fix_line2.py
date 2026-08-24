with open('deploy_server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'Top trends right now' in line:
        lines[i] = '            body = "Top trends right now:\\n\\n"\n'
        print(f'Fixed line {i+1}')
with open('deploy_server.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done')
