// src/utils/jwt.ts
import jwt_decode from 'jwt-decode';

export const decodeJWT = (token: string): any => {
  try {
    return jwt_decode(token);
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};