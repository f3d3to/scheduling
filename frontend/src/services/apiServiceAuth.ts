// src/services/apiServiceAuth.ts
const API_URL = 'http://localhost:8000';

export const api = {
    get: async (url: string) => await handleRequest(url, 'GET'),
    post: async (url: string, body?: any) => await handleRequest(url, 'POST', body),
    put: async (url: string, body?: any) => await handleRequest(url, 'PUT', body),
    delete: async (url: string) => await handleRequest(url, 'DELETE'),
    patch: async (url: string, body?: any) => await handleRequest(url, 'PATCH', body),
    getExcel: async (url: string) => await handleExcelRequest(url, 'GET'), // <--- NUEVO

};

const handleRequest = async (url: string, method: string, body?: any) => {
    const headers: HeadersInit = {
        'Content-Type': 'application/json',
    };

    // Agregar token si existe
    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    // console.log("BODY: ",body
    const config: RequestInit = {
        method,
        headers,
        body: body ? JSON.stringify(body) : null,
    };

    let response = await fetch(`${API_URL}/${url}`, config);

    // Manejar refresh token
    if (response.status === 401) {
        const newToken = await refreshToken();
        if (newToken) {
            headers['Authorization'] = `Bearer ${newToken}`;
            response = await fetch(`${API_URL}/${url}`, config);
        }
    }

    if (!response.ok) throw new Error(await response.text());

    return {
        data: await response.json(),
        status: response.status,
    };
};

const handleExcelRequest = async (url: string, method: string) => {
    const headers: HeadersInit = {};
    // Agregar token si existe
    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const config: RequestInit = {
        method,
        headers,
    };

    let response = await fetch(`${API_URL}/${url}`, config);

    // Manejar refresh token
    if (response.status === 401) {
        const newToken = await refreshToken();
        if (newToken) {
            headers['Authorization'] = `Bearer ${newToken}`;
            response = await fetch(`${API_URL}/${url}`, config);
        }
    }

    if (!response.ok) throw new Error(await response.text());

    return {
        data: await response.blob(),
        status: response.status,
        headers: response.headers,
    };
};

const refreshToken = async (): Promise<string | null> => {
    try {
        const refresh = localStorage.getItem('refresh_token');
        if (!refresh) return null;

        const response = await fetch(`${API_URL}/token/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh }),
        });

        if (!response.ok) throw new Error('Token refresh failed');

        const { access } = await response.json();
        localStorage.setItem('access_token', access);
        return access;
    } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        return null;
    }
};

// Nueva función para verificar el token
export const verifyToken = async (token: string): Promise<boolean> => {
  try {
    const response = await api.post('token/verify/', { token });
    return response.status === 200;
  } catch (error) {
    console.error('Token verification failed:', error);
    return false;
  }
};