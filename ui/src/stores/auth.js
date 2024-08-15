import { defineStore } from 'pinia';
import { useBoardStore } from '../stores/board'
import { api } from '../boot/axios'
import { useLocalStorage } from '@vueuse/core'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: useLocalStorage('user', {}),
    signUpLogin: { name:"", password:"", passwordConfirm: "" }
  }),
  getters: {
    isLoggedIn: (state) => { if ('name' in state.user && state.user.name !== "") { return true} else { return false }},
  },
  actions: {
    signOut() {
      const boardStore = useBoardStore()
      boardStore.clear()
      this.user = null
    },
    async create(body) {
      /*{
        "name": "kyt82",
        "email": "user@example.com",
        "nickname": "Kpy738s"
      }*/
      body.nickname = body.name
      var good = await api.post("/user", body)
      if (!good) {
        console.error(good)
      }
    },
    async getByName(name) {
      var good = await api.get("/user", { params: { user_name: name }})
      if (!good) {
        console.error(good)
        return
      }
      this.user = good.data
    }
  },
});
