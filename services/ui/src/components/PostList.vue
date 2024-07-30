<template>
  <div class="q-pa-md q-gutter-md">
    <q-list bordered class="rounded-borders">
      <q-item-label header>Friends</q-item-label>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/avatar2.jpg">
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label lines="1">Brunch this weekend?</q-item-label>
          <q-item-label caption lines="2">
            <span class="text-weight-bold">Janet</span>
            -- I'll be in your neighborhood doing errands this
            weekend. Do you want to grab brunch?
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
import { watch, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useBoardStore } from '../stores/board'
const boardStore = useBoardStore()
const route = useRoute()
var category = boardStore.categoryById(route.params.category)
watch(
    () => route.params.category,
    (newId, oldId) => {
      category = boardStore.categoryById(newId)
    }
  )
</script>
