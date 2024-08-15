import { defineStore } from 'pinia';
import { api } from '../boot/axios'
import { useLocalStorage } from '@vueuse/core'
import { useAuthStore } from './auth';
import urlUtil from 'src/utilities/url-util';

export const usePostStore = defineStore('post', {
  state: () => ({
    posts: [],
    createPost: useLocalStorage('createPost', {}),
    selectedPost: {}
  }),
  getters: {
    getById: (state) => (id) => {
      console.log(id)
      var post = state.posts.find(x => x.id === id)
      return post
    }
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
    selectById(postId) {
      this.selectedPost = this.posts.find(x => x.id === postId)
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
    },
    navigate(boardName, categoryName, postId) {
      var categoryEncode = urlUtil.urlEncode(categoryName)
      var boardDecode = urlUtil.urlEncode(boardName)
      var path = "/board/" + boardDecode + "/category/" + categoryEncode + "/post/" + postId
      this.$router.push(path)
    }
  },
});
