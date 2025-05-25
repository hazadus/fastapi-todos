/**
 * Конфигурация API
 */
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || "",
  ENDPOINTS: {
    AUTH: {
      LOGIN: "/api/v1/auth/login",
      SIGNUP: "/api/v1/auth/signup",
      ME: "/api/v1/auth/me",
    },
    TASKS: {
      LIST: "/api/v1/tasks",
      CREATE: "/api/v1/tasks",
      UPDATE: (id: number) => `/api/v1/tasks/${id}`,
      DELETE: (id: number) => `/api/v1/tasks/${id}`,
    },
  },
} as const;

/**
 * Создает полный URL для API endpoint
 */
export const createApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};
