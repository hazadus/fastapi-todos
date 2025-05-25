<script setup lang="ts">
/*
 * Компонент для создания новой задачи
 */
import { ref } from "vue";
import { useTasksStore } from "../stores/tasks";
import type { TaskCreate } from "../types/Task";

const tasksStore = useTasksStore();

// Состояние формы
const title = ref("");
const description = ref("");
const errorMessage = ref("");
const isSubmitting = ref(false);

// Валидация формы
const validateForm = (): boolean => {
  errorMessage.value = "";

  if (!title.value.trim()) {
    errorMessage.value = "Название задачи обязательно";
    return false;
  }

  if (title.value.trim().length < 2) {
    errorMessage.value = "Название должно содержать минимум 2 символа";
    return false;
  }

  if (title.value.trim().length > 255) {
    errorMessage.value = "Название не должно превышать 255 символов";
    return false;
  }

  if (description.value.trim().length > 5000) {
    errorMessage.value = "Описание не должно превышать 5000 символов";
    return false;
  }

  return true;
};

// Очистка формы
const clearForm = (): void => {
  title.value = "";
  description.value = "";
  errorMessage.value = "";
};

// Обработка отправки формы
const handleSubmit = async (): Promise<void> => {
  if (!validateForm()) {
    return;
  }

  isSubmitting.value = true;
  errorMessage.value = "";

  try {
    const taskData: TaskCreate = {
      title: title.value.trim(),
      description: description.value.trim() || undefined,
    };

    await tasksStore.createTask(taskData);
    clearForm();
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "Произошла ошибка при создании задачи";
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="bg-white rounded-lg shadow-lg p-6 mb-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-4">
      <i class="fas fa-plus-circle text-indigo-600 mr-2"></i>
      Создать новую задачу
    </h2>

    <form
      @submit.prevent="handleSubmit"
      class="space-y-4"
    >
      <!-- Поле названия задачи -->
      <div>
        <label
          for="title"
          class="block text-sm font-medium text-gray-700 mb-1"
        >
          Название задачи <span class="text-red-500">*</span>
        </label>
        <input
          id="title"
          v-model="title"
          type="text"
          placeholder="Введите название задачи"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          :disabled="isSubmitting"
          maxlength="255"
        />
        <p class="mt-1 text-xs text-gray-500">{{ title.length }}/255 символов</p>
      </div>

      <!-- Поле описания задачи -->
      <div>
        <label
          for="description"
          class="block text-sm font-medium text-gray-700 mb-1"
        >
          Описание (необязательно)
        </label>
        <textarea
          id="description"
          v-model="description"
          rows="3"
          placeholder="Введите описание задачи"
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 resize-none"
          :disabled="isSubmitting"
          maxlength="5000"
        ></textarea>
        <p class="mt-1 text-xs text-gray-500">{{ description.length }}/5000 символов</p>
      </div>

      <!-- Сообщение об ошибке -->
      <div
        v-if="errorMessage || tasksStore.error"
        class="text-red-600 text-sm"
      >
        <i class="fas fa-exclamation-circle mr-1"></i>
        {{ errorMessage || tasksStore.error }}
      </div>

      <!-- Кнопки действий -->
      <div class="flex space-x-3">
        <button
          type="submit"
          :disabled="isSubmitting || tasksStore.isLoading"
          class="flex-1 bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          <i
            v-if="isSubmitting || tasksStore.isLoading"
            class="fas fa-spinner fa-spin mr-2"
          ></i>
          <i
            v-else
            class="fas fa-plus mr-2"
          ></i>
          {{ isSubmitting || tasksStore.isLoading ? "Создание..." : "Создать задачу" }}
        </button>

        <button
          type="button"
          @click="clearForm"
          :disabled="isSubmitting || tasksStore.isLoading"
          class="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
        >
          <i class="fas fa-times mr-2"></i>
          Очистить
        </button>
      </div>
    </form>
  </div>
</template>
