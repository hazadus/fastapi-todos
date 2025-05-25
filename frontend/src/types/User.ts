/**
 * Интерфейс для создания пользователя
 */
export interface UserCreate {
  email: string;
  password: string;
}

/**
 * Интерфейс для обновления информации о пользователе
 */
export interface UserUpdate {
  email?: string;
  password?: string;
}

/**
 * Интерфейс для ответа с информацией о пользователе
 */
export interface User {
  id: number;
  email: string;
  created_at: string; // date string
  updated_at: string; // date string
}
