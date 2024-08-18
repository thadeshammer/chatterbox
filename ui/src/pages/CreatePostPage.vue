<template>
<q-page>
  <q-input v-model="postStore.createPost.name" label="Title"/>
  <q-input
    v-model="postStore.createPost.content"
    filled
    type="textarea"
  />
  <q-btn @click="createPost()" label="Submit"/>
</q-page>
</template>
<script setup>
import { usePostStore } from 'src/stores/post';
import { useCategoryStore } from 'src/stores/category';
import { useBoardStore } from 'src/stores/board';
import urlUtil from 'src/utilities/url-util';
import { useRoute } from 'vue-router';
const route = useRoute()
const postStore = usePostStore()
const categoryStore = useCategoryStore()
const boardStore = useBoardStore()
boardStore.getAll()
const boardDecode = urlUtil.urlDecode(route.params.board)
const board = boardStore.getByName(boardDecode)
categoryStore.get(board)
const categoryDecode = urlUtil.urlDecode(route.params.category)
function createPost() {
  console.log(categoryStore)
  console.log(categoryDecode)
  const category = categoryStore.getByName(categoryDecode)
  var post = {
    category_id: category.id,
    board_id: board.id
  }
  postStore.create(post)
  this.isCreatePost = false
}
</script>
