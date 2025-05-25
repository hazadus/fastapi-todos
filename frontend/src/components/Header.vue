<script setup lang="ts">
/*
 * Компонент заголовка для приложения
 */
import { useAuthStore } from "../stores/auth";
const authStore = useAuthStore();
</script>

<template>
  <header class="p-4 bg-indigo-700 text-white">
    <nav class="flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <i class="fas fa-tasks text-xl"></i>
        <h1>Список задач</h1>
      </div>
      <div class="flex-1 flex justify-center">
        <ul class="flex space-x-4">
          <template v-if="!authStore.isAuthenticated">
            <li>
              <router-link
                to="/"
                class="hover:underline"
                active-class="text-yellow-300 font-semibold"
                exact
                >Главная</router-link
              >
            </li>
            <li>
              <router-link
                to="/signup"
                class="hover:underline"
                active-class="text-yellow-300 font-semibold"
                >Регистрация</router-link
              >
            </li>
            <li>
              <router-link
                to="/login"
                class="hover:underline"
                active-class="text-yellow-300 font-semibold"
                >Войти</router-link
              >
            </li>
          </template>
          <template v-else>
            <li>
              <router-link
                to="/"
                class="hover:underline"
                active-class="text-yellow-300 font-semibold"
                >Задачи</router-link
              >
            </li>
            <li>
              <button
                @click="authStore.logout()"
                class="hover:underline text-red-300"
              >
                Выйти
              </button>
            </li>
          </template>
        </ul>
      </div>
      <div
        v-if="authStore.isAuthenticated"
        class="flex items-center space-x-2"
      >
        <i class="fas fa-user text-sm"></i>
        <span class="text-sm">{{ authStore.user?.email }}</span>
      </div>
    </nav>
  </header>
</template>
