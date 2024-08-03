import { defineStore } from 'pinia';

export const useBoardStore = defineStore('board', {
  state: () => ({
    categories: [
      { name: "Category 1", id: "category-1",
        posts: [
          { title: "Cat 1 Post 1", id: "cat-1-post-1", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
          { title: "Cat 1 Post 2", id: "cat-1-post-2", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
          { title: "Cat 1 Post 3", id: "cat-1-post-3", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}
      ]},
      { name: "Category 2", id: "category-2",
        posts: [
        { title: "Cat 2 Post 1", id: "cat-1-post-1", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        { title: "Cat 2 Post 2", id: "cat-1-post-2", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        { title: "Cat 2 Post 3", id: "cat-1-post-3", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}
      ]},
      { name: "Category 3", id: "category-3",
        posts: [
        { title: "Cat 3 Post 1", id: "cat-1-post-1", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        { title: "Cat 3 Post 2", id: "cat-1-post-2", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        { title: "Cat 3 Post 3", id: "cat-1-post-3", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}
      ]},
    ]
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
