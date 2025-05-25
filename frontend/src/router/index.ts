import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SignupView from "../views/SignupView.vue";
import LoginView from "../views/LoginView.vue";

const routes = [
  { path: "/", name: "Home", component: HomeView },
  { path: "/signup", name: "Signup", component: SignupView },
  { path: "/login", name: "Login", component: LoginView },
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
