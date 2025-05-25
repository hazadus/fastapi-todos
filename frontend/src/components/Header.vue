<script setup lang="ts">
/*
 * Компонент заголовка для приложения
 */
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
        </ul>
      </div>
    </nav>
  </header>
</template>
