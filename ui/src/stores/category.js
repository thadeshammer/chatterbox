import { defineStore } from 'pinia';
import { api } from '../boot/axios'

export const useCategoryStore = defineStore('category', {
  state: () => ({
    categories: null
  }),
  getters: {
    isLoggedIn: (state) => { if (state.user === null) { return false} else { return true }},
  },
  actions: {
    async create(body) {
      /*{
        "name": "string",
        "description": "string",
        "user_id": "string",
        "board_id": "string"
      }*/
      var good = await api.post("/category", body)
    },
    async get(board) {
      var good = await api.get("/category", { params: { board_id: board.id }})
      if (!good) {
        console.log(good)
        return
      }
      this.categories = good.data
    }
  },
});
