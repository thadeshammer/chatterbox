<template>
  <div class="q-pa-md q-gutter-md">
    <q-list bordered class="rounded-borders">
      <q-item-label header>{{ category.name }}</q-item-label>

      <q-item clickable v-ripple v-for="post in category.posts">
        <q-item-section avatar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/avatar2.jpg">
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label lines="1">{{ post.title }}</q-item-label>
          <q-item-label caption lines="2">
            {{ post.body }}
          </q-item-label>
        </q-item-section>

        <q-item-section side top>
          1 min ago
        </q-item-section>

        <q-separator inset="item" />
      </q-item>
    </q-list>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useBoardStore } from '../stores/board'
const boardStore = useBoardStore()
const route = useRoute()
const category = computed(() => { return boardStore.categoryById(route.params.category)} )
</script>
