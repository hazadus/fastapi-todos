import { createPinia } from "pinia";
import { createApp } from "vue";
import App from "./App.vue";
import "./assets/styles/index.css";
import router from "./router";

const app = createApp(App);
const pinia = createPinia();

// Обязательно подключаем Pinia до роутера
app.use(pinia);
app.use(router).mount("#app");
