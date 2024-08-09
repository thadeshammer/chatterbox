import { defineStore } from 'pinia';

export const useCategoryStore = defineStore('category', {
  state: () => ({
    categories: null
  }),
  getters: {
    isLoggedIn: (state) => { if (state.user === null) { return false} else { return true }},
  },
  actions: {
    create(body) {
      /*{
        "name": "string",
        "description": "string",
        "user_id": "string",
        "board_id": "string"
      }*/
      var good = api.post("/create/category", body)
    }
  },
});
