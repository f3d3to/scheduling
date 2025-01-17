Activar un Filtro:

    El usuario activa un filtro desde la UI.
    El filtro actualiza el store y realiza una solicitud al backend.

Procesamiento en el Backend:

    El backend aplica la lógica de los filtros y genera un nuevo conjunto de datos para el grafo.

Actualizar el Store:

    El frontend recibe los datos del backend y actualiza el store.

Redibujar el Grafo:

    El grafo en el frontend se redibuja automáticamente según los nuevos datos del store.

--------------
export const useFilterStore = defineStore("filters", {
  state: () => ({
    filters: {} as Record<string, any>
  }),
  actions: {
    initializeFilters(filterData: any) {
      // Convertir la lista de filtros en un objeto indexado por 'key'
      this.filters = filterData.filters.reduce((acc: any, filter: any) => {
        acc[filter.key] = filter;
        return acc;
      }, {});
    },
    toggleFilter(key: string) {
      if (this.filters[key]) {
        this.filters[key].applied = !this.filters[key].applied;
      }
    },
    updateFilterValue(key: string, value: any) {
      if (this.filters[key] && this.filters[key].type === "range") {
        this.filters[key].value = value;
      }
    },
    getActiveFilters() {
      return Object.values(this.filters).filter((filter) => filter.applied);
    }
  }
});

{
  "filters": [
    {
      "key": "approved",
      "type": "boolean",
      "applied": false,
      "description": "Mostrar materias aprobadas",
      "endpoint": "/api/materias?filter=approved"
    },
    {
      "key": "elective",
      "type": "boolean",
      "applied": true,
      "description": "Mostrar materias electivas",
      "endpoint": "/api/materias?filter=elective"
    },
    {
      "key": "year",
      "type": "range",
      "applied": false,
      "description": "Filtrar por año",
      "min": 1,
      "max": 5,
      "value": [1, 3],
      "endpoint": "/api/materias?filter=year"
    }
  ]
}


--------------
Gracias por señalarlo. Ahora que tenemos claro que la estructura del JSON debe incluir los datos completos de nodos, enlaces, materias y materia estudiante, ajustemos la representación para cumplir con esos requisitos, sin olvidar lo discutido previamente.

---

### **JSON Revisado con Todos los Datos**

```json
{
  "materias": [
    {
      "id": "materia-1",
      "nombre": "Matemática",
      "anio": 1,
      "creditos": 6,
      "correlativas": ["materia-2", "materia-3"]
    },
    {
      "id": "materia-2",
      "nombre": "Física",
      "anio": 1,
      "creditos": 4,
      "correlativas": ["materia-3"]
    }
  ],
  "materias_estudiantes": [
    {
      "id": "materia-estudiante-1",
      "materia_id": "materia-1",
      "estado": "aprobada",
      "nota_final": 8.5
    }
  ],
  "nodos": [
    {
      "id": "node-1",
      "materia_id": "materia-1",
      "label": "Matemática",
      "visual": {
        "color": "#1f77b4",
        "shape": "circle",
        "size": 10
      }
    },
    {
      "id": "node-2",
      "materia_id": "materia-2",
      "label": "Física",
      "visual": {
        "color": "#ff7f0e",
        "shape": "square",
        "size": 12
      }
    },
    {
      "id": "node-3",
      "materia_estudiante_id": "materia-estudiante-1",
      "label": "Matemática (Estudiante)",
      "visual": {
        "color": "#2ca02c",
        "shape": "triangle",
        "size": 8
      }
    }
  ],
  "links": [
    {
      "source": "node-1",
      "target": "node-2",
      "type": "correlativa",
      "visual": {
        "color": "#999",
        "width": 2,
        "style": "solid"
      }
    },
    {
      "source": "node-1",
      "target": "node-3",
      "type": "relacion_estudiante",
      "visual": {
        "color": "#555",
        "width": 1,
        "style": "dashed"
      }
    }
  ],
  "filters": [
    {
      "key": "approved",
      "type": "boolean",
      "applied": false,
      "description": "Mostrar materias aprobadas",
      "endpoint": "/api/materias?filter=approved"
    },
    {
      "key": "elective",
      "type": "boolean",
      "applied": true,
      "description": "Mostrar materias electivas",
      "endpoint": "/api/materias?filter=elective"
    }
  ]
}
```

---

### **Detalles Adicionales**

1. **Materias y MateriasEstudiantes**:
   - **`materias`**: Contiene toda la información relacionada con las materias del plan de estudios.
   - **`materias_estudiantes`**: Información específica de cada estudiante relacionada con sus materias, como `estado` y `nota_final`.

2. **Nodos (`nodos`)**:
   - Contienen referencias a `materias` o `materias_estudiantes` a través de `materia_id` o `materia_estudiante_id`.
   - Las propiedades en `visual` son exclusivamente para la representación gráfica.

3. **Enlaces (`links`)**:
   - Relacionan nodos entre sí, con referencias a sus `source` y `target` (`id` de los nodos).
   - Las propiedades en `visual` son para personalizar la apariencia de los enlaces.

4. **Filtros (`filters`)**:
   - Representan las opciones de filtrado disponibles, incluyendo su estado (`applied`) y un `endpoint` para ejecutar el filtro.

---

### **Flujo Esperado**

1. **Backend**:
   - Genera el JSON dinámico, combinando `materias`, `materias_estudiantes`, nodos y enlaces, basándose en los filtros recibidos del frontend.

2. **Pinia**:
   - Almacena los datos de manera estructurada:
     - `materias` y `materias_estudiantes` para lógica de dominio.
     - `nodos` y `links` para la representación visual.
   - Permite actualizar dinámicamente el grafo al aplicar o cambiar filtros.

3. **Componente del Grafo**:
   - Consume los datos directamente del store.
   - Redibuja los nodos y enlaces utilizando las propiedades en `visual`.

---

### **Ventajas del Enfoque**

1. **Separación Clara**:
   - Los datos visuales (`nodos`, `links`) están completamente separados de la lógica de dominio (`materias`, `materias_estudiantes`).

2. **Extensibilidad**:
   - Nuevos filtros, atributos o tipos de nodos pueden integrarse fácilmente.

3. **Flexibilidad en Visualización**:
   - La personalización visual está aislada en las propiedades `visual`.

