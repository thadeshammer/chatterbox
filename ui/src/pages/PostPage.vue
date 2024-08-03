<template>
  <q-page>
    <div class="text-h3">{{ post.title }}</div>
  </q-page>
</template>
<script setup>
import { useRoute } from 'vue-router'
import { useBoardStore } from 'src/stores/board';
const route = useRoute()
const boardStore = useBoardStore()
const post = boardStore.postById(route.params.category, route.params.id)
</script>
