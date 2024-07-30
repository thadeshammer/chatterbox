import { defineStore } from 'pinia';

export const useBoardStore = defineStore('board', {
  state: () => ({
    categories: [
      {name: "Category 1", id: "category-1"},
      {name: "Category 2", id: "category-2"},
      {name: "Category 3", id: "category-3"}
    ],
  }),
  getters: {
    doubleCount: (state) => state.counter * 2,
    categoryById: (state) => (id) => state.categories.find(x => x.id === id)
  },
  actions: {
    increment() {
      this.counter++;
    },
  },
});
