<script setup lang="ts">
/*
 * Компонент для отображения списка задач
 */
import { computed, ref } from "vue";
import { useTasksStore } from "../stores/tasks";
import TaskItem from "./TaskItem.vue";

const tasksStore = useTasksStore();

// Фильтры для задач
const filter = ref<"all" | "pending" | "completed">("all");

// Вычисляемые списки задач
const filteredTasks = computed(() => {
  switch (filter.value) {
    case "pending":
      return tasksStore.pendingTasks;
    case "completed":
      return tasksStore.completedTasks;
    default:
      return tasksStore.tasks;
  }
});

// Статистика
const stats = computed(() => ({
  total: tasksStore.totalTasks,
  completed: tasksStore.completedTasks.length,
  pending: tasksStore.pendingTasks.length,
}));

// Смена фильтра
const setFilter = (newFilter: "all" | "pending" | "completed") => {
  filter.value = newFilter;
};
</script>

<template>
  <div class="bg-white rounded-lg shadow-lg">
    <!-- Заголовок и фильтры -->
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold text-gray-900">
          <i class="fas fa-list-ul text-indigo-600 mr-2"></i>
          Мои задачи
        </h2>

        <!-- Статистика -->
        <div class="flex items-center space-x-4 text-sm text-gray-600">
          <span class="flex items-center">
            <i class="fas fa-tasks mr-1"></i>
            Всего: {{ stats.total }}
          </span>
          <span class="flex items-center text-yellow-600">
            <i class="fas fa-clock mr-1"></i>
            В процессе: {{ stats.pending }}
          </span>
          <span class="flex items-center text-green-600">
            <i class="fas fa-check-circle mr-1"></i>
            Выполнено: {{ stats.completed }}
          </span>
        </div>
      </div>

      <!-- Фильтры -->
      <div class="flex space-x-1">
        <button
          @click="setFilter('all')"
          :class="{
            'bg-indigo-600 text-white': filter === 'all',
            'bg-gray-100 text-gray-700 hover:bg-gray-200': filter !== 'all',
          }"
          class="px-4 py-2 rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          <i class="fas fa-list mr-1"></i>
          Все задачи
        </button>

        <button
          @click="setFilter('pending')"
          :class="{
            'bg-indigo-600 text-white': filter === 'pending',
            'bg-gray-100 text-gray-700 hover:bg-gray-200': filter !== 'pending',
          }"
          class="px-4 py-2 rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          <i class="fas fa-clock mr-1"></i>
          В процессе ({{ stats.pending }})
        </button>

        <button
          @click="setFilter('completed')"
          :class="{
            'bg-indigo-600 text-white': filter === 'completed',
            'bg-gray-100 text-gray-700 hover:bg-gray-200': filter !== 'completed',
          }"
          class="px-4 py-2 rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          <i class="fas fa-check-circle mr-1"></i>
          Выполнено ({{ stats.completed }})
        </button>
      </div>
    </div>

    <!-- Список задач -->
    <div class="p-6">
      <!-- Состояние загрузки -->
      <div
        v-if="tasksStore.isLoading && tasksStore.tasks.length === 0"
        class="flex items-center justify-center py-12"
      >
        <div class="flex items-center space-x-3 text-indigo-600">
          <i class="fas fa-spinner fa-spin text-xl"></i>
          <span class="text-lg">Загрузка задач...</span>
        </div>
      </div>

      <!-- Ошибка -->
      <div
        v-else-if="tasksStore.error"
        class="flex items-center justify-center py-12"
      >
        <div class="text-center">
          <i class="fas fa-exclamation-triangle text-red-500 text-3xl mb-3"></i>
          <p class="text-red-600 text-lg mb-2">Ошибка загрузки задач</p>
          <p class="text-gray-600 text-sm">{{ tasksStore.error }}</p>
          <button
            @click="tasksStore.fetchTasks()"
            class="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
          >
            <i class="fas fa-redo mr-2"></i>
            Попробовать снова
          </button>
        </div>
      </div>

      <!-- Пустой список -->
      <div
        v-else-if="filteredTasks.length === 0"
        class="text-center py-12"
      >
        <div class="text-gray-400 mb-4">
          <i
            :class="{
              'fas fa-inbox': filter === 'all',
              'fas fa-clock': filter === 'pending',
              'fas fa-check-circle': filter === 'completed',
            }"
            class="text-4xl mb-3"
          ></i>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">
          {{
            filter === "all"
              ? "Пока нет задач"
              : filter === "pending"
              ? "Нет задач в процессе"
              : "Нет выполненных задач"
          }}
        </h3>
        <p class="text-gray-600">
          {{
            filter === "all"
              ? "Создайте свою первую задачу, чтобы начать организовывать дела"
              : filter === "pending"
              ? "Все задачи выполнены! Отличная работа!"
              : "Завершите задачи, чтобы увидеть их здесь"
          }}
        </p>
      </div>

      <!-- Список задач -->
      <div
        v-if="filteredTasks.length > 0"
        class="space-y-4"
      >
        <TaskItem
          v-for="task in filteredTasks"
          :key="task.id"
          :task="task"
        />
      </div>
    </div>

    <!-- Футер со сводкой -->
    <div
      v-if="stats.total > 0 && !tasksStore.isLoading"
      class="px-6 py-4 bg-gray-50 border-t border-gray-200 rounded-b-lg"
    >
      <div class="flex items-center justify-between text-sm text-gray-600">
        <span>
          Показано {{ filteredTasks.length }} из {{ stats.total }}
          {{ stats.total === 1 ? "задачи" : stats.total < 5 ? "задач" : "задач" }}
        </span>

        <div
          v-if="stats.completed > 0"
          class="flex items-center space-x-2"
        >
          <div class="w-24 bg-gray-200 rounded-full h-2">
            <div
              class="bg-green-500 h-2 rounded-full"
              :style="{ width: `${(stats.completed / stats.total) * 100}%` }"
            ></div>
          </div>
          <span class="text-green-600 font-medium">
            {{ Math.round((stats.completed / stats.total) * 100) }}% выполнено
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
