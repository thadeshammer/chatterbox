<template>
  <q-page class="flex column">
    <div class="text-h3">
      {{ route.params.category }}
    </div>
    <div class="row">
      <q-space/>
      <q-btn @click="postStore.navigateCreate(route.params.board, route.params.category)" label="Create Post"/>
    </div>
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
var boardDecode = urlUtil.urlDecode(route.params.board)
init()
watch(
  () => route.params.category,
  (newId, oldId) => {
    categoryDecode = urlUtil.urlDecode(newId)
  }
)
watch(
  () => route.params.board,
  (newId, oldId) => {
    boardDecode = urlUtil.urlDecode(newId)
    init()
  }
)


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

