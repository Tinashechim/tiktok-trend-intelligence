content = open('deploy_server.py', 'r', encoding='utf-8').read()

# Check if movement endpoint has names
if 'MOVEMENT_NAMES' not in content:
    # Add movement naming constants before the movement endpoint
    movement_code = '''
MOVEMENT_NAMES = {
    "peace_sign": {"name": "Peace Sign", "source": "comments"},
    "hands_up_jumping": {"name": "Jumping Hands Up", "source": "local_lingo"},
    "pointing": {"name": "Pointing", "source": "comments"},
    "head_nod": {"name": "Head Nod", "source": "comments"},
    "fist_pump": {"name": "Fist Pump", "source": "local_lingo"},
}
'''
    # Insert before the existing movement endpoint
    old_movement = '@app.get("/api/trends/movement")'
    if old_movement in content:
        content = content.replace(old_movement, movement_code + '\n' + old_movement)
    
    open('deploy_server.py', 'w', encoding='utf-8').write(content)
    print('Movement naming added')
else:
    print('Movement naming already present')
