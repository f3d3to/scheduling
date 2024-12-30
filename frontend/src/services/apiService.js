export async function fetchPlans() {
  const response = await fetch("http://localhost:8000/planes_de_estudio/");
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }
  return await response.json();
}

export async function fetchCycles(planId) {
  const response = await fetch(`http://localhost:8000/planes/${planId}/ciclos/`);
  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }
  return await response.json();
}

  export async function fetchCorrelatives(nodeId) {
    const response = await fetch(`http://localhost:8000/materias/${nodeId}/correlativas/`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  }


const API_URL = 'http://localhost:8000';

export async function fetchModels() {
  try {
    const response = await fetch(`${API_URL}/estructura-modelos/`);
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  } catch (error) {
    console.error('There was a problem fetching model data:', error);
  }
}
