<script setup lang="ts">
/*
 * Страница входа в аккаунт
 */
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

const authStore = useAuthStore();
const router = useRouter();

const handleSubmit = async () => {
  // Сброс ошибок
  errorMessage.value = "";

  // Валидация данных
  if (!email.value.trim()) {
    errorMessage.value = "Email обязателен для заполнения";
    return;
  }

  if (!password.value.trim()) {
    errorMessage.value = "Пароль обязателен для заполнения";
    return;
  }

  // Проверка формата email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.value)) {
    errorMessage.value = "Введите корректный email адрес";
    return;
  }

  if (password.value.length < 8) {
    errorMessage.value = "Пароль должен содержать минимум 8 символов";
    return;
  }

  isLoading.value = true;

  try {
    await authStore.login({
      email: email.value.trim(),
      password: password.value,
    });

    // Перенаправление на главную страницу при успешном входе
    await router.push("/");
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : "Произошла ошибка при входе";
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="min-h-[calc(100vh-6rem)] flex items-center justify-center">
    <div class="max-w-md w-full">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Войти в аккаунт</h2>
        <p class="mt-2 text-center text-sm text-gray-600">Введите ваши данные для входа</p>
      </div>

      <form
        @submit.prevent="handleSubmit"
        class="mt-8 space-y-6"
      >
        <!-- Отображение ошибок -->
        <div
          v-if="errorMessage"
          class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded"
        >
          {{ errorMessage }}
        </div>

        <div class="space-y-4">
          <div>
            <label
              for="email"
              class="block text-sm font-medium text-gray-700"
            >
              Email
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              :disabled="isLoading"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm disabled:bg-gray-100"
              placeholder="Введите ваш email"
            />
          </div>

          <div>
            <label
              for="password"
              class="block text-sm font-medium text-gray-700"
            >
              Пароль
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              :disabled="isLoading"
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm disabled:bg-gray-100"
              placeholder="Введите пароль"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            <i
              v-if="!isLoading"
              class="fas fa-sign-in-alt mr-2"
            ></i>
            <i
              v-else
              class="fas fa-spinner fa-spin mr-2"
            ></i>
            {{ isLoading ? "Вход..." : "Войти" }}
          </button>
        </div>

        <div class="text-center">
          <router-link
            to="/signup"
            class="font-medium text-indigo-600 hover:text-indigo-500"
          >
            Нет аккаунта? Зарегистрироваться
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>
