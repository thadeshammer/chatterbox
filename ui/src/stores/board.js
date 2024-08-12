import { defineStore } from 'pinia';
import { api } from 'src/boot/axios';
import { useAuthStore } from './auth';
import { useCategoryStore } from './category';
import { useLocalStorage } from '@vueuse/core'

export const useBoardStore = defineStore('board', {
  state: () => ({
    boardCreate: {},
    boards: useLocalStorage('boards', []),
  }),
  getters: {
    getByName: (state) => (name) => {
      var board = state.boards.find(x => x.name === name)
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
    init() {
      if (this.categories != null) {
        return
      }
    }
  },
});
