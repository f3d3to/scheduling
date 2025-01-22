import requests
import json

def login(username, password):
    """Realiza el login y devuelve el token JWT."""
    try:
        response = requests.post(
            "http://localhost:8000/token/",
            headers={"Content-Type": "application/json"},
            json={"username": username, "password": password},
        )
        response.raise_for_status()
        return response.json()["access"]
    except requests.exceptions.RequestException as e:
        print(f"Error al iniciar sesión: {e}")
        return None

def get_user_data(user_id, token):
    """Obtiene los datos del usuario usando el token JWT."""
    try:
        response = requests.get(
            f"http://localhost:8000/usuarios/{user_id}/",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos del usuario: {e}")
        return None

def main():
    """Función principal para probar la API."""

    # Login
    token = login("user", "user")  # Cambiar por credenciales validas si es necesario.
    if token:
        print(f"Token JWT obtenido: {token[:50]}...")

        # Obtener datos del usuario (reemplazar con un ID de usuario válido)
        user_data = get_user_data(1, token) # Usar un user id que exista.
        if user_data:
            print("Datos del usuario:")
            print(json.dumps(user_data, indent=4))

if __name__ == "__main__":
    main()