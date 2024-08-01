import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: { username: "Jake" },
    signUpLogin: { username:"", password:"", passwordConfirm: "" }
  }),
  getters: {
    isLoggedIn: (state) => { if (state.user === null) { return false} else { return true }},
  },
  actions: {
    signOut() {
      this.user = null
    }
  },
});
