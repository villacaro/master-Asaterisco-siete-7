path = 'admin_AsteriscoSiete-server/admin_AsteriscoSiete7/admin_asterisco7/templates/arrejuntao/index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("import('./firebase-auth.js')", "import('/static/arrejuntao/firebase-auth.js')")

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Fixed!')
