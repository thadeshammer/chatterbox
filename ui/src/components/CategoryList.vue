<template>
  <div class="q-pa-md q-gutter-md">
    <q-list padding style="max-width: 350px">
      <q-item-label header>Categories</q-item-label>

      <q-item clickable v-ripple @click="categoryNav(category.name)" v-for="category in categoryStore.categories">
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
import { useRoute, useRouter } from 'vue-router'
const categoryStore = useCategoryStore()
const router = useRouter()
const route = useRoute()
function categoryNav(name) {
  router.push('/board/' + route.params.board + '/category/' + name)
}
</script>
