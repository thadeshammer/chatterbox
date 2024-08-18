<template>
  <div style="min-height: 100%" class="row">
    <board-icon-list></board-icon-list>
    <q-list padding style="max-width: 350px">
      <q-item-label header class="text-grey-4">Categories</q-item-label>

      <q-item clickable v-ripple @click="categoryStore.navigate(route.params.board, category.name)" v-for="category in categoryStore.categories">
        <q-item-section avatar top>
          <q-avatar icon="folder" color="primary" text-color="white" />
        </q-item-section>

        <q-item-section>
          <q-item-label lines="1">{{ category.name }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script setup>
import { useCategoryStore } from 'src/stores/category';
import { useRoute } from 'vue-router'
import BoardIconList from './BoardIconList.vue';
const categoryStore = useCategoryStore()
const route = useRoute()

</script>
