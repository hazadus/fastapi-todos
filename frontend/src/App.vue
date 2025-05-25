<script setup lang="ts">
import Header from "./components/Header.vue";
import { useAuthStore } from "./stores/auth";

// Загрузка пользователя из локального хранилища
const authStore = useAuthStore();
authStore.loadUserFromStorage();
</script>

<template>
  <div
    id="app"
    class="max-w-7xl mx-auto"
  >
    <Header />
    <main class="p-4">
      <router-view />
    </main>
  </div>
</template>
