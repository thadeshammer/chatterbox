import { defineStore } from 'pinia';
import { api } from '../boot/axios'
import { useLocalStorage } from '@vueuse/core'
import urlUtil from 'src/utilities/url-util';

export const useCategoryStore = defineStore('category', {
  state: () => ({
    categories: [],
    selectedCategory: useLocalStorage('selectedCategory', {})
  }),
  getters: {
    isLoggedIn: (state) => { if (state.user === null) { return false} else { return true }},
    getById: (state) => (id) => state.categories.find(x => x.id === id),
    getByName: (state) => (name) => state.categories.find(x => x.name === name)
  },
  actions: {
    select(category) {
      this.selectedCategory = category
    },
    async create(body) {
      /*{
        "name": "string",
        "description": "string",
        "user_id": "string",
        "board_id": "string"
      }*/
      var good = await api.post("/category", body)
      if (!good) {
        console.error(good)
        return
      }
      this.categories = good.data
    },
    async get(board) {
      var good = await api.get("/category", { params: { board_id: board.id }})
      if (!good) {
        console.log(good)
        return
      }
      this.categories = good.data
    },
    navigate(boardName, categoryName) {
      var boardEncode = urlUtil.urlEncode(boardName)
      var categoryEncode = urlUtil.urlEncode(categoryName)
      var path =  '/board/' + boardEncode + '/category/' + categoryEncode
      this.$router.push(path)
    }
  },
});
