import { defineStore } from 'pinia';
import { useBoardStore } from '../stores/board'

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
      const boardStore = useBoardStore()
      boardStore.clear()
      this.user = null
    }
  },
});
