import { defineStore } from 'pinia';
import { api } from 'src/boot/axios';
import { useAuthStore } from './auth';
import { useCategoryStore } from './category';
import { useLocalStorage } from '@vueuse/core'
import { useRoute } from 'vue-router';
import urlUtil from '../utilities/url-util'

export const useBoardStore = defineStore('board', {
  state: () => ({
    boardCreate: {},
    boards: useLocalStorage('boards', []),
    route: useRoute()
  }),
  getters: {
    getByName: (state) => (name) => {
      var board = state.boards.find(x => x.name === name)
      return board
    },
    getFromRoute: (state) => () => {
      const boardDecode = urlUtil.urlDecode(state.route.params.board)
      var board = state.boards.find(x => x.name === boardDecode)
      return board
    }
  },
  actions: {
    increment() {
      this.counter++;
    },
    clear() {
      this.categories = []
    },
    async create(body){
      /*{
        "name": "dimwits collective",
        "description": "just dimwits things",
        "user_id": "user-bb772355-37ce-469c-ace2-7630d4f876f4"
      }*/
      var authStore = useAuthStore()
      body.user_id = authStore.user.id
      var good = await api.post("/board", body)
      if (!good) {
        console.error(good)
      }
      this.boards.push(good.data.board)
      var category = {
        name: "Main",
        description: "default category",
        user_id: authStore.user.id,
        board_id: good.data.board.id
      }
      var categoryStore = useCategoryStore()
      categoryStore.create(category)
    },
    async getAll() {
      var good = await api.get("/board")
      if (!good) {
        console.error(good)
        this.boards = []
        return
      }
      this.boards = good.data
    },
    async navigate(board) {
      var enc = urlUtil.urlEncode(board.name)
      await this.categoryStore.get(board)
      var categoryEnc = urlUtil.urlEncode(this.categoryStore.categories[0].name)
      if (this.categoryStore.categories.length > 0) {
        var path = '/board/' + enc + '/category/' + categoryEnc
        this.$router.push(path)
      }
    },
    navigateAdmin() {

      var path = '/board/' + this.route.params.board + '/admin'
      this.$router.push(path)
    },
    init() {
      if (this.categories != null) {
        return
      }
    }
  },
});
