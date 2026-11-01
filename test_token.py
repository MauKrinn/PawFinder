from supabase import create_client
from backend.core.config import settings

# Conectamos con Supabase usando tus credenciales del .env
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

email = "pruebawhatsapp@pawfinder.com"
password = "passwordSeguro123"

try:
    # Intentamos registrar al usuario
    res = supabase.auth.sign_up({"email": email, "password": password})
    print("\n✅ USUARIO CREADO CON ÉXITO")
except Exception:
    # Si ya existe, iniciamos sesión
    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    print("\n✅ LOGIN EXITOSO")

print("\n🔑 COPIA ESTE TOKEN JWT (Es la cadena larga, sin comillas ni espacios extra):")
print(res.session.access_token)
print("\n")