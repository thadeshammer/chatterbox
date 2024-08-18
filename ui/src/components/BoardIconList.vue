<template>
  <div class="bg-grey-10">
    <q-list style="max-width: 64px">

      <q-item
      style="cursor:pointer"
      clickable
      no-ripple
      @click="boardStore.navigate(board)"
      class="q-pa-sm bg-grey-10"
      v-for="board in boardStore.boards">
        <q-tooltip class="bg-grey-10" anchor="center right" self="center left" :offset="[10, 10]">
          {{ board.name }}
        </q-tooltip>
        <q-item-section>
          <q-avatar size="40px" icon="folder" color="primary" text-color="grey-4" />
        </q-item-section>
      </q-item>

    </q-list>
  </div>
</template>

<script setup>
import { useBoardStore } from 'src/stores/board';
import { useRoute } from 'vue-router'
const boardStore = useBoardStore()
const route = useRoute()

</script>

<style>
.q-btn .q-focus-helper {
  display: none;
}
</style>
