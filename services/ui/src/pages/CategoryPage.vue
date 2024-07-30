<template>
  <q-page class="flex flex-center">
    {{ thing.categoryId }}
  </q-page>
</template>

<script setup>
import { watch, reactive } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()
const thing = reactive({ categoryId: route.params.category})
watch(
    () => route.params.category,
    (newId, oldId) => {
      // react to route changes...
      console.log(newId);
      thing.categoryId = newId
    }
  )
defineOptions({
  name: 'CategoryPage'
});
</script>

