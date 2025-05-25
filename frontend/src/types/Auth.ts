import { type User } from "./User";

/**
 * Интерфейс для запроса регистрации пользователя
 */
export interface SignupRequest {
  email: string;
  password: string;
}

/**
 * Интерфейс для ответа с информацией о зарегистрированном пользователе
 */
export interface SignupResponse {
  user: User;
  message: string;
}

/**
 * Интерфейс для запроса входа пользователя
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Интерфейс для ответа с информацией о вошедшем пользователе
 */
export interface LoginResponse {
  user: User;
  access_token: string;
  token_type: string;
}
