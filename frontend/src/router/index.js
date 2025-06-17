import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Phonenumbers from "../views/Phonenumbers.vue";
import Login from "../views/Login.vue";
import Section from "../views/Sections.vue";
import PhoneTypes from "../views/PhoneTypes.vue";
import Users from "../views/Users.vue";
import Jobs from "../views/Jobs.vue";
import About from "../views/About.vue";
import { useAuthStore } from "@/store/auth";

const routes = [
  { path: "/", name: "Home", component: Home },
  {
    path: "/phonenumbers",
    name: "phonenumbers",
    component: Phonenumbers,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  { path: "/login", name: "login", component: Login },
  {
    path: "/sections",
    name: "sections",
    component: Section,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/phonetypes",
    name: "phonetypes",
    component: PhoneTypes,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/users",
    name: "users",
    component: Users,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/jobs",
    name: "jobs",
    component: Jobs,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: "/forbidden",
    name: "forbidden",
    component: () => import("../components/Forbidden.vue"),
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: () => import("../views/NotFound.vue"), // Create this file optionally
  },
     { path: "/about", name: "About", component: About }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next("/login");
  } else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next("/forbidden");
  } else {
    next();
  }
});

export default router;
