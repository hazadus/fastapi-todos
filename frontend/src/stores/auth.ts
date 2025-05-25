/**
 * Pinia store для управления аутентификацией пользователей
 */
import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { API_CONFIG, createApiUrl } from "../config/api";
import type { LoginRequest, LoginResponse, SignupRequest, SignupResponse } from "../types/Auth";
import type { User } from "../types/User";

export const useAuthStore = defineStore("auth", () => {
  // State
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);
  const isAuthenticated = ref<boolean>(false);

  // Getters
  const isLoggedIn = computed(() => isAuthenticated.value && !!token.value && !!user.value);

  // Actions
  const login = async (credentials: LoginRequest): Promise<void> => {
    try {
      const response = await fetch(createApiUrl(API_CONFIG.ENDPOINTS.AUTH.LOGIN), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка входа");
      }

      const data: LoginResponse = await response.json();

      // Сохраняем данные в state
      user.value = data.user;
      token.value = data.access_token;
      isAuthenticated.value = true;

      // Сохраняем токен в localStorage
      localStorage.setItem("auth_token", data.access_token);
      localStorage.setItem("user_data", JSON.stringify(data.user));
    } catch (error) {
      console.error("Ошибка при входе:", error);
      throw error;
    }
  };

  const signup = async (userData: SignupRequest): Promise<void> => {
    try {
      const response = await fetch(createApiUrl(API_CONFIG.ENDPOINTS.AUTH.SIGNUP), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка регистрации");
      }

      const data: SignupResponse = await response.json();
      console.log("Пользователь зарегистрирован:", data.message);
    } catch (error) {
      console.error("Ошибка при регистрации:", error);
      throw error;
    }
  };

  const logout = (): void => {
    // Очищаем state
    user.value = null;
    token.value = null;
    isAuthenticated.value = false;

    // Удаляем данные из localStorage
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user_data");
  };

  const loadUserFromStorage = (): void => {
    try {
      const savedToken = localStorage.getItem("auth_token");
      const savedUserData = localStorage.getItem("user_data");

      if (savedToken && savedUserData) {
        token.value = savedToken;
        user.value = JSON.parse(savedUserData);
        isAuthenticated.value = true;
      }
    } catch (error) {
      console.error("Ошибка при загрузке данных из localStorage:", error);
      // Очищаем поврежденные данные
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user_data");
    }
  };

  const getCurrentUser = async (): Promise<void> => {
    if (!token.value) {
      throw new Error("Токен не найден");
    }

    try {
      const response = await fetch(createApiUrl(API_CONFIG.ENDPOINTS.AUTH.ME), {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token.value}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          // Токен истек или недействителен
          logout();
          throw new Error("Сессия истекла");
        }
        throw new Error("Ошибка получения данных пользователя");
      }

      const userData: User = await response.json();
      user.value = userData;
      localStorage.setItem("user_data", JSON.stringify(userData));
    } catch (error) {
      console.error("Ошибка при получении данных пользователя:", error);
      throw error;
    }
  };

  return {
    // State
    user,
    token,
    isAuthenticated,
    // Getters
    isLoggedIn,
    // Actions
    login,
    signup,
    logout,
    loadUserFromStorage,
    getCurrentUser,
  };
});
