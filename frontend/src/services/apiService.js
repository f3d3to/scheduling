// apiService.js
const API_URL = 'http://localhost:8000';

async function handleRequest(url, method = 'GET', data = null) {
  const headers = new Headers({
    'Content-Type': 'application/json',
  });

  // Obtiene el token del localStorage
  const token = localStorage.getItem('access_token');
  // Agrega el token al encabezado Authorization si existe
  if (token) {
    headers.append('Authorization', `Bearer ${token}`);
  }

  const config = {
    method,
    headers,
    body: data ? JSON.stringify(data) : null,
  };

  const response = await fetch(`${API_URL}/${url}`, config);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HTTP error! status: ${response.status}, ${errorText}`);
  }

  return response.json(); // asumiendo que todas las respuestas son JSON
}

// apiService.js

export async function fetchPlans() {
  return handleRequest('planes_de_estudio/');
}

export async function fetchCycles(planId) {
  return handleRequest(`planes/${planId}/ciclos/`);
}

export async function fetchCorrelatives(nodeId) {
  return handleRequest(`materias/${nodeId}/correlativas/`);
}

export async function fetchModels() {
  return handleRequest('estructura-modelos/');
}