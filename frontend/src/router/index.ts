import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import NotFoundView from "../views/NotFoundView.vue";
import SignupView from "../views/SignupView.vue";
import TasksView from "../views/TasksView.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/signup", name: "Signup", component: SignupView },
  { path: "/login", name: "Login", component: LoginView },
  { path: "/tasks", name: "Tasks", component: TasksView },
  // Catch-all маршрут для 404 страницы (должен быть последним)
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFoundView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    // Всегда прокручивать к верху страницы
    return { top: 0 };
  },
});

export default router;
