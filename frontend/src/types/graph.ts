export interface Node {
    id: string;
    name: string;
    year: number | "Sin año";
    color?: string;
    size?: number;
    cssClass?: string;
    materiaData?: Materia; // Tipo del backend
    estudianteData?: MateriaEstudiante; // Si aplica
  }

  export interface Link {
    source: string;
    target: string;
    strokeWidth?: number;
    strokeColor?: string;
  }

  // Tipos para respuestas API (ajusta según tus modelos Django)
  export interface Plan {
    id: string;
    nombre: string;
    año_creacion: number;
  }

  export interface ApiResponse<T> {
    results: T[];
  }

  export interface Celda {
    id: number;
    contenido: string;
    coordenadas: string;
    w?: number;
    h?: number;
    [key: string]: any;
  }

  export interface Layout {
    i: string;
    x: number;
    y: number;
    w: number;
    h: number;
  }