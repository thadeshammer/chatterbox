<template>
  <q-page class="flex column">
    <q-input v-if="isCreatePost" v-model="postStore.createPost.title" label="Title"/>
    <q-input v-if="isCreatePost" v-model="postStore.createPost.body" label="Body"/>
    <q-btn v-if="isCreatePost" @click="createPost()" label="Submit"/>
    <q-btn v-if="!isCreatePost" @click="isCreatePost = true" label="Create Post"/>
    <component :is="PostList"/>
  </q-page>
</template>

<script setup>
import { watch, ref, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import PostList from '../components/PostList.vue'
import { useCategoryStore } from 'src/stores/category'
import { useBoardStore } from 'src/stores/board'
import { usePostStore } from 'src/stores/post'
import urlUtil from 'src/utilities/url-util'

const categoryStore = useCategoryStore()
const boardStore = useBoardStore()
const postStore = usePostStore()
const route = useRoute()
const isCreatePost = ref(false)
const categoryDecode = urlUtil.urlDecode(route.params.category)
const boardDecode = urlUtil.urlDecode(route.params.board)
init()
watch(
    () => route.params.category,
    (newId, oldId) => {
      category = categoryStore.getByName(categoryDecode)
    }
  )
function createPost() {
  var post = {
    title: postStore.createPost.title,
    body: postStore.createPost.body,
    category_id: categoryStore.getByName(categoryDecode).id,
    board_id: boardStore.getByName(boardDecode).id
  }
  postStore.create(post)
  this.isCreatePost = false
}

async function init() {
  if (categoryStore.categories.length === 0) {
      await categoryStore.get(boardStore.getByName(boardDecode))
    }
  await postStore.get(categoryStore.getByName(categoryDecode))
}
defineOptions({
  name: 'CategoryPage'
});
</script>

