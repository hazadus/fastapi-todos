/**
 * Pinia store для управления задачами пользователей
 */
import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { API_CONFIG, createApiUrl } from "../config/api";
import type { Task, TaskCreate, TaskUpdate, TaskListResponse } from "../types/Task";
import { useAuthStore } from "./auth";

export const useTasksStore = defineStore("task", () => {
  // State
  const tasks = ref<Task[]>([]);
  const isLoading = ref<boolean>(false);
  const error = ref<string | null>(null);

  // Getters
  const completedTasks = computed(() => tasks.value.filter((task) => task.is_completed));
  const pendingTasks = computed(() => tasks.value.filter((task) => !task.is_completed));
  const totalTasks = computed(() => tasks.value.length);

  // Helper function to get auth headers
  const getAuthHeaders = () => {
    const authStore = useAuthStore();
    if (!authStore.token) {
      throw new Error("Токен авторизации не найден");
    }
    return {
      Authorization: `Bearer ${authStore.token}`,
      "Content-Type": "application/json",
    };
  };

  // Actions
  const fetchTasks = async (): Promise<void> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(createApiUrl(API_CONFIG.ENDPOINTS.TASKS.LIST), {
        method: "GET",
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка получения задач");
      }

      const data: TaskListResponse = await response.json();
      tasks.value = data.tasks;
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Неизвестная ошибка";
      console.error("Ошибка при получении задач:", err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const createTask = async (taskData: TaskCreate): Promise<Task> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(createApiUrl(API_CONFIG.ENDPOINTS.TASKS.CREATE), {
        method: "POST",
        headers: getAuthHeaders(),
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка создания задачи");
      }

      const newTask: Task = await response.json();
      tasks.value.push(newTask);
      return newTask;
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Неизвестная ошибка";
      console.error("Ошибка при создании задачи:", err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateTask = async (taskId: number, taskData: TaskUpdate): Promise<Task> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(createApiUrl(API_CONFIG.ENDPOINTS.TASKS.UPDATE(taskId)), {
        method: "PATCH",
        headers: getAuthHeaders(),
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка обновления задачи");
      }

      const updatedTask: Task = await response.json();

      // Обновляем задачу в массиве
      const taskIndex = tasks.value.findIndex((task) => task.id === taskId);
      if (taskIndex !== -1) {
        tasks.value[taskIndex] = updatedTask;
      }

      return updatedTask;
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Неизвестная ошибка";
      console.error("Ошибка при обновлении задачи:", err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const deleteTask = async (taskId: number): Promise<void> => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(createApiUrl(API_CONFIG.ENDPOINTS.TASKS.DELETE(taskId)), {
        method: "DELETE",
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Ошибка удаления задачи");
      }

      // Удаляем задачу из массива
      tasks.value = tasks.value.filter((task) => task.id !== taskId);
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Неизвестная ошибка";
      console.error("Ошибка при удалении задачи:", err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const toggleTaskCompletion = async (taskId: number): Promise<Task> => {
    const task = tasks.value.find((t) => t.id === taskId);
    if (!task) {
      throw new Error("Задача не найдена");
    }

    return await updateTask(taskId, { is_completed: !task.is_completed });
  };

  const clearError = (): void => {
    error.value = null;
  };

  const clearTasks = (): void => {
    tasks.value = [];
    error.value = null;
    isLoading.value = false;
  };

  return {
    // State
    tasks,
    isLoading,
    error,
    // Getters
    completedTasks,
    pendingTasks,
    totalTasks,
    // Actions
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    clearError,
    clearTasks,
  };
});
