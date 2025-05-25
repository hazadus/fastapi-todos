<script setup lang="ts"></script>

<template>
  <div class="min-h-[calc(100vh-6rem)] flex items-center justify-center">
    <div class="max-w-2xl w-full text-center px-4">
      <div class="mb-8">
        <i class="fas fa-tasks text-6xl text-indigo-600 mb-4"></i>
        <h1 class="text-4xl font-extrabold text-gray-900 mb-4">Добро пожаловать в Список задач!</h1>
        <p class="text-xl text-gray-600 mb-8">
          Управляйте своими задачами легко и эффективно. Создавайте, редактируйте и отслеживайте прогресс
          ваших дел.
        </p>
      </div>

      <div class="space-y-4">
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <router-link
            to="/login"
            class="inline-flex items-center justify-center px-6 py-3 border border-transparent text-lg font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
          >
            <i class="fas fa-sign-in-alt mr-2"></i>
            Войти
          </router-link>

          <router-link
            to="/signup"
            class="inline-flex items-center justify-center px-6 py-3 border border-indigo-600 text-lg font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-150 ease-in-out"
          >
            <i class="fas fa-user-plus mr-2"></i>
            Зарегистрироваться
          </router-link>
        </div>

        <p class="text-sm text-gray-500 mt-4">Начните организовывать свои задачи уже сегодня</p>
      </div>

      <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="text-center">
          <div class="bg-white rounded-lg p-6 shadow-lg h-full">
            <i class="fas fa-plus-circle text-3xl text-indigo-600 mb-3"></i>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Создавайте</h3>
            <p class="text-gray-600">Легко добавляйте новые задачи с описанием</p>
          </div>
        </div>

        <div class="text-center">
          <div class="bg-white rounded-lg p-6 shadow-lg h-full">
            <i class="fas fa-edit text-3xl text-indigo-600 mb-3"></i>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Редактируйте</h3>
            <p class="text-gray-600">Обновляйте задачи прямо в списке</p>
          </div>
        </div>

        <div class="text-center">
          <div class="bg-white rounded-lg p-6 shadow-lg h-full">
            <i class="fas fa-check-circle text-3xl text-indigo-600 mb-3"></i>
            <h3 class="text-lg font-semibold text-gray-900 mb-2">Отслеживайте</h3>
            <p class="text-gray-600">Фильтруйте и сортируйте выполненные задачи</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
