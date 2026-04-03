import os
import re

root_index = 'index.html'

with open(root_index, 'r', encoding='utf-8') as f:
    text = f.read()

# Extract the <!-- ─── PANTALLA DE LOGIN ─── --> section from root index.html
match = re.search(r'(<!-- ─── PANTALLA DE LOGIN ─── -->.*?</script>)\s*<!-- ─── APP SHELL ─── -->', text, re.DOTALL)
if not match:
    print("Could not find PANTALLA DE LOGIN in root index.html")
    exit(1)

new_login_screen = match.group(1)

def exact_replace(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # regex to remove ANY OLD login screen
    # Old login screen has <div id="login-screen" ... "Lotería · Triple 7" or similar
    # New login screen has <div id="login-screen"...
    
    # We will just find <body ...> and <!-- APP SHELL --> and replace everything between them with new login screen!
    body_match = re.search(r'(<body[^>]*>)\s*', content, re.IGNORECASE)
    shell_match = re.search(r'(<!--[^\n]*APP SHELL[^\n]*-->)', content, re.IGNORECASE)
    
    if body_match and shell_match:
        before = content[:body_match.end()]
        after = content[shell_match.start():]
        new_content = before + "\n\n" + new_login_screen + "\n\n\n" + after
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Re-wrote login screen in {filepath}")
    else:
        print(f"Could not rewrite {filepath}")

exact_replace('appelarrejuntao-main/index.html')
exact_replace('appelarrejuntao-main/public/index.html')
exact_replace('admin_AsteriscoSiete-server/admin_AsteriscoSiete7/admin_asterisco7/templates/arrejuntao/index.html')
