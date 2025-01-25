// types/auth.ts

export interface Usuario {
    id: number;
    username: string;
    email: string;
    perfil?: string;  // Opcional porque puede ser null/blank en Django
    firstName?: string;  // Si extiendes el modelo con first_name
    lastName?: string;   // Si extiendes el modelo con last_name
    isStaff?: boolean;   // Si necesitas manejar permisos de staff
    isSuperuser?: boolean; // Para usuarios administradores
    dateJoined?: string;  // Fecha de registro (ISO string)
    lastLogin?: string;   // Último inicio de sesión (ISO string)
}

// Tipo para la respuesta de autenticación
export interface AuthResponse {
    access: string;
    refresh: string;
    user: Usuario;
}

// Tipo para el payload del JWT (puedes personalizarlo según tus necesidades)
export interface JwtPayload {
    userId: number;
    username: string;
    email: string;
    exp: number;  // Timestamp de expiración
    iat: number;  // Timestamp de emisión
}