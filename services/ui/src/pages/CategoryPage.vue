<template>
  <q-page class="flex column">
    <component :is="PostList"/>
  </q-page>
</template>

<script setup>
import { watch, ref } from 'vue'
import { useRoute } from 'vue-router'
import PostList from '../components/PostList.vue'
import { useBoardStore } from '../stores/board'
const boardStore = useBoardStore()
const route = useRoute()
var category = boardStore.categoryById(route.params.category)
watch(
    () => route.params.category,
    (newId, oldId) => {
      category = boardStore.categoryById(route.params.category)
    }
  )
defineOptions({
  name: 'CategoryPage'
});
</script>

