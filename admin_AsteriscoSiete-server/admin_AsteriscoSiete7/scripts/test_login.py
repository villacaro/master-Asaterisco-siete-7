import requests

session = requests.Session()
login_url = "https://master-asterisco-siete-7-production.up.railway.app/admin/login/?next=/dashboard/"
response = session.get(login_url)

csrf_token = session.cookies.get('csrftoken')
if not csrf_token:
    print("No CSRF token found!")
    exit(1)

payload = {
    'csrfmiddlewaretoken': csrf_token,
    'username': 'admin',
    'password': 'Asterisco2026!',
    'next': '/dashboard/'
}
headers = {
    'Referer': login_url
}
post_response = session.post(login_url, data=payload, headers=headers)

if "Por favor introduzca el nombre de usuario y la clave correctos" in post_response.text:
    print("Login Failed")
else:
    print("Login Success")
