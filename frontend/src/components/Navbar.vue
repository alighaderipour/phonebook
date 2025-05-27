<template>
  <nav class="navbar">
    <div class="nav-left">
      <router-link to="/" class="nav-link">صفحه اصلی</router-link>


      <router-link to="/phonenumbers" class="nav-link"
                   v-if="authStore.isLoggedIn && authStore.isAdmin">
        شماره تلفن ها
      </router-link>

      <router-link to="/sections" class="nav-link"
                   v-if="authStore.isLoggedIn && authStore.isAdmin">
        بخش ها
      </router-link>

      <router-link to="/phonetypes" class="nav-link"
                   v-if="authStore.isLoggedIn && authStore.isAdmin">
        نوع شماره تلفن
      </router-link>

      <router-link to="/users" class="nav-link"
                   v-if="authStore.isLoggedIn && authStore.isAdmin">
        کاربران
      </router-link>

      <router-link to="/jobs" class="nav-link"
                   v-if="authStore.isLoggedIn && authStore.isAdmin">
        شغل ها
      </router-link>
       <router-link to="/about" class="nav-link">درباره</router-link>
    </div>

    <div class="nav-right">
      <router-link to="/login" class="nav-link" v-if="!authStore.isLoggedIn">
        ورود
      </router-link>
      <button v-if="authStore.isLoggedIn" @click="logout" class="logout-button">
        خروج
      </button>
    </div>
  </nav>
</template>


<script>
import { useAuthStore } from '@/store/auth';

export default {
  name: 'Navbar',
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  methods: {
    logout() {
      this.authStore.logout();
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.navbar {
  background-color: #2c3e50;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left,
.nav-right {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  color: #ecf0f1;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #3498db;
}

.logout-button {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #c0392b;
}
</style>
