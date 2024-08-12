import { defineStore } from 'pinia';
import { api } from '../boot/axios'
import { useLocalStorage } from '@vueuse/core'
import { useAuthStore } from './auth';
import { useBoardStore } from './board';

export const usePostStore = defineStore('post', {
  state: () => ({
    posts: [],
    createPost: useLocalStorage('createPost', {})
  }),
  getters: {
  },
  actions: {
    async create(post) {
      var authStore = useAuthStore()
      var req = {
        name: post.title,
        content: post.body,
        user_id: authStore.user.id,
        board_id: post.board_id,
        category_id: post.category_id
      }
      var good = await api.post("/post", req)
      if (!good) {
        console.error(good)
        return
      }
    },
    async get(category) {
      if (!category) {
        console.warn("Category is: ", category)
        return
      }
      var good = await api.get('/post', {params:{ category_id: category.id }})
      if (!good) {
        console.error(good)
        return
      }
      this.posts = good.data
    }
  },
});
