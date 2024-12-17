export async function fetchCycles() {
    const response = await fetch("http://localhost:8000/planes/1/ciclos/");
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
