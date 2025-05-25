<script setup lang="ts">
/*
 * Компонент для работы со списком задач пользователя
 */
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import TaskForm from "../components/TaskForm.vue";
import TaskList from "../components/TaskList.vue";
import { useAuthStore } from "../stores/auth";
import { useTasksStore } from "../stores/tasks";

const authStore = useAuthStore();
const tasksStore = useTasksStore();

// Редирект на страницу логина, если пользователь не аутентифицирован
if (!authStore.isAuthenticated) {
  useRouter().push("/");
}

// Загружаем задачи после монтирования компонента
onMounted(async () => {
  await tasksStore.fetchTasks();
});
</script>

<template>
  <div class="space-y-6">
    <TaskForm />
    <TaskList />
  </div>
</template>
