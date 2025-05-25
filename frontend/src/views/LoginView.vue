<script setup lang="ts">
/*
 * Страница входа в аккаунт
 */
import { ref } from "vue";

const email = ref("");
const password = ref("");

const handleSubmit = () => {
  console.log("Email:", email.value);
  console.log("Password:", password.value);
  // Здесь будет логика входа
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
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
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
              class="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Введите пароль"
            />
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
          >
            <i class="fas fa-sign-in-alt mr-2"></i>
            Войти
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
