import { defineStore } from 'pinia';

export const useCommentStore = defineStore('comment', {
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
        "content": "string",
        "user_id": "string",
        "category_id": "string"
      }*/
      var good = api.post("/create/comment", body)
    }
  },
});
