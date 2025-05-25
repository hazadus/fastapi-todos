<script setup lang="ts">
/*
 * Компонент для отображения одной задачи
 */
import { computed, ref } from "vue";
import { useTasksStore } from "../stores/tasks";
import type { Task } from "../types/Task";

interface Props {
  task: Task;
}

const props = defineProps<Props>();
const tasksStore = useTasksStore();

// Состояние редактирования
const isEditingTitle = ref(false);
const isEditingDescription = ref(false);
const editTitle = ref(props.task.title);
const editDescription = ref(props.task.description || "");
const isUpdating = ref(false);

// Форматирование даты
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

// Вычисляемые свойства
const taskClasses = computed(() => ({
  "opacity-60": props.task.is_completed,
  "border-green-200 bg-green-50": props.task.is_completed,
  "border-gray-200 bg-white": !props.task.is_completed,
}));

const titleClasses = computed(() => ({
  "line-through text-gray-500": props.task.is_completed,
  "text-gray-900": !props.task.is_completed,
}));

// Переключение статуса задачи
const toggleCompletion = async (): Promise<void> => {
  try {
    await tasksStore.toggleTaskCompletion(props.task.id);
  } catch (error) {
    console.error("Ошибка при изменении статуса задачи:", error);
  }
};

// Удаление задачи
const deleteTask = async (): Promise<void> => {
  if (!confirm("Вы уверены, что хотите удалить эту задачу?")) {
    return;
  }

  try {
    await tasksStore.deleteTask(props.task.id);
  } catch (error) {
    console.error("Ошибка при удалении задачи:", error);
  }
};

// Начало редактирования заголовка
const startEditingTitle = (): void => {
  if (props.task.is_completed) return;

  editTitle.value = props.task.title;
  isEditingTitle.value = true;
};

// Начало редактирования описания
const startEditingDescription = (): void => {
  if (props.task.is_completed) return;

  editDescription.value = props.task.description || "";
  isEditingDescription.value = true;
};

// Сохранение изменений заголовка
const saveTitle = async (): Promise<void> => {
  const newTitle = editTitle.value.trim();

  if (!newTitle) {
    editTitle.value = props.task.title;
    isEditingTitle.value = false;
    return;
  }

  if (newTitle === props.task.title) {
    isEditingTitle.value = false;
    return;
  }

  if (newTitle.length > 255) {
    alert("Название не должно превышать 255 символов");
    return;
  }

  isUpdating.value = true;

  try {
    await tasksStore.updateTask(props.task.id, { title: newTitle });
    isEditingTitle.value = false;
  } catch (error) {
    console.error("Ошибка при обновлении заголовка:", error);
    editTitle.value = props.task.title;
  } finally {
    isUpdating.value = false;
  }
};

// Сохранение изменений описания
const saveDescription = async (): Promise<void> => {
  const newDescription = editDescription.value.trim();

  if (newDescription === (props.task.description || "")) {
    isEditingDescription.value = false;
    return;
  }

  if (newDescription.length > 5000) {
    alert("Описание не должно превышать 5000 символов");
    return;
  }

  isUpdating.value = true;

  try {
    await tasksStore.updateTask(props.task.id, {
      description: newDescription || undefined,
    });
    isEditingDescription.value = false;
  } catch (error) {
    console.error("Ошибка при обновлении описания:", error);
    editDescription.value = props.task.description || "";
  } finally {
    isUpdating.value = false;
  }
};

// Отмена редактирования
const cancelEditTitle = (): void => {
  editTitle.value = props.task.title;
  isEditingTitle.value = false;
};

const cancelEditDescription = (): void => {
  editDescription.value = props.task.description || "";
  isEditingDescription.value = false;
};

// Обработка нажатия клавиш
const handleTitleKeydown = (event: KeyboardEvent): void => {
  if (event.key === "Enter") {
    event.preventDefault();
    saveTitle();
  } else if (event.key === "Escape") {
    cancelEditTitle();
  }
};

const handleDescriptionKeydown = (event: KeyboardEvent): void => {
  if (event.key === "Enter" && event.ctrlKey) {
    event.preventDefault();
    saveDescription();
  } else if (event.key === "Escape") {
    cancelEditDescription();
  }
};
</script>

<template>
  <div
    class="border rounded-lg p-4 shadow-sm transition-all duration-200 hover:shadow-md"
    :class="taskClasses"
  >
    <!-- Заголовок задачи -->
    <div class="flex items-start space-x-3 mb-3">
      <!-- Чекбокс -->
      <label class="flex items-center cursor-pointer mt-1">
        <input
          type="checkbox"
          :checked="task.is_completed"
          @change="toggleCompletion"
          :disabled="tasksStore.isLoading || isUpdating"
          class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded disabled:cursor-not-allowed"
        />
      </label>

      <!-- Заголовок -->
      <div class="flex-1 min-w-0">
        <!-- Режим просмотра заголовка -->
        <h3
          v-if="!isEditingTitle"
          @click="startEditingTitle"
          :class="titleClasses"
          class="text-lg font-medium cursor-pointer hover:bg-gray-50 rounded px-2 py-1 -mx-2 -my-1 transition-colors"
          :title="task.is_completed ? '' : 'Нажмите для редактирования'"
        >
          {{ task.title }}
        </h3>

        <!-- Режим редактирования заголовка -->
        <div
          v-else
          class="flex space-x-2"
        >
          <input
            v-model="editTitle"
            @keydown="handleTitleKeydown"
            @blur="saveTitle"
            type="text"
            class="flex-1 text-lg font-medium border border-indigo-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            maxlength="255"
            autofocus
          />
          <button
            @click="saveTitle"
            :disabled="isUpdating"
            class="px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-400 text-sm"
          >
            <i class="fas fa-check"></i>
          </button>
          <button
            @click="cancelEditTitle"
            :disabled="isUpdating"
            class="px-2 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:bg-gray-400 text-sm"
          >
            <i class="fas fa-times"></i>
          </button>
        </div>
      </div>

      <!-- Кнопка удаления -->
      <button
        @click="deleteTask"
        :disabled="tasksStore.isLoading || isUpdating"
        class="p-2 text-red-600 hover:bg-red-50 rounded focus:outline-none focus:ring-2 focus:ring-red-500 disabled:text-gray-400 disabled:cursor-not-allowed transition-colors"
        title="Удалить задачу"
      >
        <i class="fas fa-trash text-sm"></i>
      </button>
    </div>

    <!-- Описание задачи -->
    <div
      v-if="task.description || isEditingDescription"
      class="ml-7 mb-3"
    >
      <!-- Режим просмотра описания -->
      <p
        v-if="!isEditingDescription && task.description"
        @click="startEditingDescription"
        :class="{ 'line-through text-gray-400': task.is_completed }"
        class="text-gray-600 cursor-pointer hover:bg-gray-50 rounded px-2 py-1 -mx-2 -my-1 transition-colors whitespace-pre-wrap"
        :title="task.is_completed ? '' : 'Нажмите для редактирования'"
      >
        {{ task.description }}
      </p>

      <!-- Режим редактирования описания -->
      <div
        v-else-if="isEditingDescription"
        class="space-y-2"
      >
        <textarea
          v-model="editDescription"
          @keydown="handleDescriptionKeydown"
          rows="3"
          class="w-full text-gray-600 border border-indigo-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
          maxlength="5000"
          placeholder="Введите описание задачи"
          autofocus
        ></textarea>
        <div class="flex justify-between items-center">
          <p class="text-xs text-gray-500">{{ editDescription.length }}/5000 символов</p>
          <div class="flex space-x-2">
            <button
              @click="saveDescription"
              :disabled="isUpdating"
              class="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-400 text-sm"
            >
              <i class="fas fa-check mr-1"></i>
              Сохранить
            </button>
            <button
              @click="cancelEditDescription"
              :disabled="isUpdating"
              class="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 disabled:bg-gray-400 text-sm"
            >
              <i class="fas fa-times mr-1"></i>
              Отмена
            </button>
          </div>
        </div>
        <p class="text-xs text-gray-400">
          <i class="fas fa-info-circle mr-1"></i>
          Ctrl+Enter для сохранения, Esc для отмены
        </p>
      </div>
    </div>

    <!-- Кнопка добавления описания -->
    <div
      v-if="!task.description && !task.is_completed && !isEditingDescription"
      class="ml-7 mb-3"
    >
      <button
        @click="startEditingDescription"
        class="text-gray-400 hover:text-gray-600 text-sm italic hover:bg-gray-50 rounded px-2 py-1 -mx-2 -my-1 transition-colors"
      >
        <i class="fas fa-plus mr-1"></i>
        Добавить описание
      </button>
    </div>

    <!-- Информация о дате создания и статусе -->
    <div class="ml-7 flex items-center justify-between text-xs text-gray-500">
      <div class="flex items-center space-x-4">
        <span>
          <i class="fas fa-calendar-plus mr-1"></i>
          Создано: {{ formatDate(task.created_at) }}
        </span>
        <span
          v-if="task.updated_at !== task.created_at"
          class="text-gray-400"
        >
          <i class="fas fa-edit mr-1"></i>
          Изменено: {{ formatDate(task.updated_at) }}
        </span>
      </div>

      <!-- Индикатор статуса -->
      <div class="flex items-center">
        <span
          v-if="task.is_completed"
          class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
        >
          <i class="fas fa-check mr-1"></i>
          Выполнено
        </span>
        <span
          v-else
          class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800"
        >
          <i class="fas fa-clock mr-1"></i>
          В процессе
        </span>
      </div>
    </div>

    <!-- Индикатор загрузки -->
    <div
      v-if="isUpdating"
      class="absolute inset-0 bg-white bg-opacity-50 flex items-center justify-center rounded-lg"
    >
      <div class="flex items-center space-x-2 text-indigo-600">
        <i class="fas fa-spinner fa-spin"></i>
        <span class="text-sm">Сохранение...</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Дополнительные стили для плавной анимации */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Стили для чекбокса */
input[type="checkbox"]:checked {
  background-color: #4f46e5;
  border-color: #4f46e5;
}

/* Стили для текстовых полей при фокусе */
input:focus,
textarea:focus {
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}
</style>
