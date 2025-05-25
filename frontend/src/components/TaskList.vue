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

// Сортировка
const sortBy = ref<"created_at" | "status">("created_at");
const sortOrder = ref<"asc" | "desc">("desc");

// Вычисляемые списки задач
const filteredTasks = computed(() => {
  let tasks;
  switch (filter.value) {
    case "pending":
      tasks = tasksStore.pendingTasks;
      break;
    case "completed":
      tasks = tasksStore.completedTasks;
      break;
    default:
      tasks = tasksStore.tasks;
  }

  // Сортировка
  const sortedTasks = [...tasks].sort((a, b) => {
    let comparison = 0;

    if (sortBy.value === "created_at") {
      const dateA = new Date(a.created_at);
      const dateB = new Date(b.created_at);
      comparison = dateA.getTime() - dateB.getTime();
    } else if (sortBy.value === "status") {
      // Сортировка по статусу: pending (false) идет первым, completed (true) - вторым
      // Number(false) = 0, Number(true) = 1
      comparison = Number(a.is_completed) - Number(b.is_completed);
    }

    // Возвращаемое значение:
    // - Отрицательное число - a должно быть перед b
    // - Положительное число - b должно быть перед a
    return sortOrder.value === "asc" ? comparison : -comparison;
  });

  return sortedTasks;
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

// Смена сортировки
const setSortBy = (newSortBy: "created_at" | "status") => {
  sortBy.value = newSortBy;
};

// Переключение направления сортировки
const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};
</script>

<template>
  <div class="bg-white rounded-lg shadow-lg">
    <!-- Заголовок и фильтры -->
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold text-gray-900">
          <i class="fas fa-list-ul text-indigo-600 mr-2"></i>
          <span class="hidden md:inline">Мои задачи</span>
        </h2>

        <!-- Статистика -->
        <div class="flex items-center space-x-4 text-sm text-gray-600">
          <span class="flex items-center">
            <i class="fas fa-tasks mr-1"></i>
            <span class="hidden md:flex">Всего:</span> {{ stats.total }}
          </span>
          <span class="flex items-center text-yellow-600">
            <i class="fas fa-clock mr-1"></i>
            <span class="hidden md:flex">В процессе:</span> {{ stats.pending }}
          </span>
          <span class="flex items-center text-green-600">
            <i class="fas fa-check-circle mr-1"></i>
            <span class="hidden md:flex">Выполнено:</span> {{ stats.completed }}
          </span>
        </div>
      </div>

      <!-- Фильтры и сортировка -->
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-3 sm:space-y-0">
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
            Все <span class="hidden md:inline">задачи</span>
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
            <span class="hidden md:inline">В процессе</span> ({{ stats.pending }})
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
            <span class="hidden md:inline">Выполнено</span> ({{ stats.completed }})
          </button>
        </div>

        <!-- Сортировка -->
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-600">Сортировка:</span>

          <!-- Выбор критерия сортировки -->
          <div class="flex space-x-1">
            <button
              @click="setSortBy('created_at')"
              :class="{
                'bg-indigo-600 text-white': sortBy === 'created_at',
                'bg-gray-100 text-gray-700 hover:bg-gray-200': sortBy !== 'created_at',
              }"
              class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              <i class="fas fa-calendar mr-1"></i>
              По дате
            </button>

            <button
              @click="setSortBy('status')"
              :class="{
                'bg-indigo-600 text-white': sortBy === 'status',
                'bg-gray-100 text-gray-700 hover:bg-gray-200': sortBy !== 'status',
              }"
              class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              <i class="fas fa-flag mr-1"></i>
              По статусу
            </button>
          </div>

          <!-- Направление сортировки -->
          <button
            @click="toggleSortOrder"
            class="p-1.5 rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            :title="sortOrder === 'asc' ? 'По возрастанию' : 'По убыванию'"
          >
            <i
              :class="{
                'fas fa-sort-up': sortOrder === 'asc',
                'fas fa-sort-down': sortOrder === 'desc',
              }"
              class="text-sm"
            ></i>
          </button>
        </div>
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

      <!-- Список задач с анимацией -->
      <TransitionGroup
        v-if="filteredTasks.length > 0"
        name="task"
        tag="div"
        class="space-y-4"
      >
        <TaskItem
          v-for="task in filteredTasks"
          :key="task.id"
          :task="task"
        />
      </TransitionGroup>
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

<style scoped>
/* Анимации для задач */
.task-enter-active {
  transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.task-leave-active {
  transition: all 0.4s cubic-bezier(0.55, 0, 0.1, 1);
}

.task-enter-from {
  opacity: 0;
  transform: translateY(-30px) scale(0.95);
}

.task-leave-to {
  opacity: 0;
  transform: translateX(50px) scale(0.9);
}

.task-move {
  transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Дополнительные стили для плавной анимации */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>
