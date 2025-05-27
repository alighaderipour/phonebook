<template>
  <div class="container" dir="rtl">
    <div class="card">
      <h2 class="login-title">ورود</h2>
      <p style="color: #dc2626; direction: rtl; text-align: center; font-weight: bold; margin: 20px auto; font-size: 16px;">
  ورود فقط برای ادمین امکان پذیر است
</p>

      <form @submit.prevent="handleLogin" class="form">
        <input
          v-model="userID"
          type="text"
          placeholder="نام کاربری"
          required
          class="input-field"
        />
        <input
          v-model="password"
          type="password"
          placeholder="رمز عبور"
          required
          class="input-field"
        />
        <button
          type="submit"
          :disabled="loading"
          class="btn btn-primary"
          :class="{ 'loading': loading }"
        >
          {{ loading ? 'در حال ورود...' : 'ورود' }}
          <span class="button-loader" v-if="loading"></span>
        </button>
        <p class="status status-error" v-if="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { useAuthStore } from '@/store/auth'; // Pinia store

export default {
  name: 'Login',
  data() {
    return {
      userID: '',
      password: '',
      loading: false,
      error: '',
    };
  },
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = '';

      try {
        const response = await axios.post('http://192.168.8.202:5000/login', {
          UserID: this.userID,
          password: this.password,
        });

        // ✅ Store user data in Pinia state
        this.authStore.setUser(response.data);
        this.$router.push('/');
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed. Please try again.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f9fafb;
  padding: 16px;
  font-family: 'Inter', system-ui, sans-serif;
}

.card {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
  width: 100%;
  max-width: 400px;
}

.login-title {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  text-align: center;
  margin-bottom: 24px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.input-field {
  padding: 10px 12px;
  font-size: 16px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.btn {
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  position: relative;
}

.btn-primary {
  background-color: #2563eb;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background-color: #1d4ed8;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-primary.loading {
  padding-right: 40px;
}

.button-loader {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #ffffff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: translateY(-50%) rotate(360deg); }
}

.status-error {
  font-size: 14px;
  color: #dc2626;
  text-align: center;
  margin-top: 12px;
}
.input-field {
  direction: rtl;
  text-align: right;
}

</style>