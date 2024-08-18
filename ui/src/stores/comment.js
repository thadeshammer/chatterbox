import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core'
import { usePostStore } from './post';
import { useAuthStore } from './auth';
import { api } from '../boot/axios'

export const useCommentStore = defineStore('comment', {
  state: () => ({
    comments: [],
    createComment: useLocalStorage('createComment', {}),
    isCreateComment: false
  }),
  getters: {
    isLoggedIn: (state) => { if (state.user === null) { return false} else { return true }},
  },
  actions: {
    create() {
      /*{
        "content": "string",
        "user_id": "string",
        "post_id": "string"
      }*/
      var authStore = useAuthStore()
      var postStore = usePostStore()
      var body = {
        content: this.createComment.content,
        user_id: authStore.user.id,
        post_id: postStore.selectedPost.id
      }
      var good = api.post("/comment", body)
      if (!good) {
        console.error(good)
        return
      }
      this.comments = good.data
    },
    async getByPostId(postId) {
      var good = await api.get("/comment", { params: { post_id: postId} })
      if (!good) {
        console.error(good)
      }
      this.comments = good.data
    }
  },
});
