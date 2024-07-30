<template>
  <div class="q-pa-md q-gutter-md">
    <q-list padding style="max-width: 350px">
      <q-item-label header>Categories</q-item-label>

      <q-item clickable v-ripple @click="setCategory(category.id)" v-for="category in boardStore.categories">
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

<script>
import { mapStores } from 'pinia';
import { useBoardStore } from 'src/stores/board';
import { defineComponent } from 'vue';

export default defineComponent({
  computed: {
    ...mapStores(useBoardStore)
  },
  methods: {
    setCategory(id) {
      this.$router.push('/category/' + id)
    }
  }
})
</script>
