import { defineStore } from 'pinia';

export const useBoardStore = defineStore('board', {
  state: () => ({
    categories: [
      { name: "Category 1", id: "category-1",
        posts: [
          { title: "Cat 1 Post 1", urlEscaped: "cat_1_post_1", id: "1", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
          { title: "Cat 1 Post 2", urlEscaped: "cat_1_post_2", id: "2", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
          { title: "Cat 1 Post 3", urlEscaped: "cat_1_post_3", id: "3", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}
      ]},
      { name: "Category 2", id: "category-2",
        posts: [
        { title: "Cat 2 Post 1", urlEscaped: "cat_2_post_1", id: "4", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        { title: "Cat 2 Post 2", urlEscaped: "cat_2_post_2", id: "5", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        { title: "Cat 2 Post 3", urlEscaped: "cat_2_post_3", id: "6", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}
      ]},
      { name: "Category 3", id: "category-3",
        posts: [
        { title: "Cat 3 Post 1", urlEscaped: "cat_3_post_1", id: "7", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        { title: "Cat 3 Post 2", urlEscaped: "cat_3_post_2", id: "8", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."},
        { title: "Cat 3 Post 3", urlEscaped: "cat_3_post_3", id: "9", body: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}
      ]},
    ]
  }),
  getters: {
    doubleCount: (state) => state.counter * 2,
    categoryById: (state) => (id) => state.categories.find(x => x.id === id),
    postById: (state) => (categoryId, postId) => {
      var category = state.categories.find(x => x.id === categoryId)
      if (category) {
        var post = category.posts.find(x => x.id === postId)
        if (post) {
          return post
        }
      }
      return undefined
    }
  },
  actions: {
    increment() {
      this.counter++;
    },
    clear() {
      this.categories = []
    }
  },
});
