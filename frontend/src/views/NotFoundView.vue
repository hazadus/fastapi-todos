<script setup lang="ts">
/*
 * Страница 404 - страница не найдена
 */
import { useRouter } from "vue-router";

const router = useRouter();

const goHome = () => {
  router.push("/");
};

const goBack = () => {
  router.go(-1);
};
</script>

<template>
  <div class="min-h-[calc(100vh-6rem)] flex items-center justify-center">
    <div class="max-w-md w-full text-center px-4">
      <div class="mb-8">
        <i class="fas fa-exclamation-triangle text-6xl text-red-500 mb-4"></i>
        <h1 class="text-6xl font-bold text-gray-900 mb-4">404</h1>
        <h2 class="text-2xl font-semibold text-gray-700 mb-4">Страница не найдена</h2>
        <p class="text-gray-600 mb-8">
          К сожалению, запрашиваемая страница не существует или была перемещена.
        </p>
      </div>

      <div class="space-y-4">
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            @click="goHome"
            class="inline-flex items-center justify-center px-6 py-3 border border-transparent text-lg font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
          >
            <i class="fas fa-home mr-2"></i>
            На главную
          </button>

          <button
            @click="goBack"
            class="inline-flex items-center justify-center px-6 py-3 border border-indigo-600 text-lg font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
          >
            <i class="fas fa-arrow-left mr-2"></i>
            Назад
          </button>
        </div>
      </div>

      <div class="mt-8 text-sm text-gray-500">
        <p>Если вы считаете, что это ошибка, обратитесь к администратору</p>
      </div>
    </div>
  </div>
</template>
