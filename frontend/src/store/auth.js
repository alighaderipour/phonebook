import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.user,
    isAdmin: (state) => state.user?.is_admin === 1,
  },
  actions: {
    setUser(userData) {
      this.user = userData;
    },
    logout() {
      this.user = null;
    },
  },
});
