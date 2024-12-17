// Estructura para la Materia
export class Materia {
  codigo: string;
  nombre: string;
  anio: number;
  ciclo: string;
  cuatrimestre: number;
  condicion: string;
  formato_didactico: string;
  ch_semanal: number;
  ch_cuatrimestral: number;
  creditos: number;
  ch_presencial: number;
  ch_distancia: number;
  ch_total: number;
  descripcion: string | null;
  correlativas: Materia[]; // Relación de muchos a muchos con otras Materias

  constructor(
    codigo: string,
    nombre: string,
    anio: number,
    ciclo: string,
    cuatrimestre: number,
    condicion: string,
    formato_didactico: string,
    ch_semanal: number,
    ch_cuatrimestral: number,
    creditos: number,
    ch_presencial: number,
    ch_distancia: number,
    ch_total: number,
    descripcion: string | null = null,
    correlativas: Materia[] = []
  ) {
    this.codigo = codigo;
    this.nombre = nombre;
    this.anio = anio;
    this.ciclo = ciclo;
    this.cuatrimestre = cuatrimestre;
    this.condicion = condicion;
    this.formato_didactico = formato_didactico;
    this.ch_semanal = ch_semanal;
    this.ch_cuatrimestral = ch_cuatrimestral;
    this.creditos = creditos;
    this.ch_presencial = ch_presencial;
    this.ch_distancia = ch_distancia;
    this.ch_total = ch_total;
    this.descripcion = descripcion;
    this.correlativas = correlativas;
  }
}

// Estructura para el PlanDeEstudio
export class PlanDeEstudio {
  id: string;
  nombre: string;
  año_creacion: number;
  descripcion: string;
  materias: Materia[];

  constructor(
    id: string,
    nombre: string,
    año_creacion: number,
    descripcion: string,
    materias: Materia[] = []
  ) {
    this.id = id;
    this.nombre = nombre;
    this.año_creacion = año_creacion;
    this.descripcion = descripcion;
    this.materias = materias;
  }
}

// Estructura para representar un nodo de Materia en GoJS
export class MateriaNode {
  key: string;
  name: string;
  creditos: number;
  ciclo: string;
  group: string;
  strikethrough: boolean;

  constructor(
    key: string,
    name: string,
    creditos: number,
    ciclo: string,
    group: string,
    strikethrough: boolean
  ) {
    this.key = key;
    this.name = name;
    this.creditos = creditos;
    this.ciclo = ciclo;
    this.group = group;
    this.strikethrough = strikethrough;
  }
}
