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
  },
} as const;

/**
 * Создает полный URL для API endpoint
 */
export const createApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};
