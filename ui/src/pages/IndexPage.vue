<template>
  <q-page class="flex flex-center">
    <q-input v-if="createBoard" v-model="boardStore.boardCreate.name" label="Name" />
    <q-input v-if="createBoard" v-model="boardStore.boardCreate.description" label="Description" />
    <q-btn v-if="!createBoard" @click="createBoard = !createBoard" label="Create Board"/>
    <q-btn v-if="createBoard" @click="boardStore.create(boardStore.boardCreate); createBoard = !createBoard" label="Confirm" />
  </q-page>
</template>

<script setup>
import { useBoardStore } from 'src/stores/board';
import { useAuthStore } from 'src/stores/auth';
import { ref } from 'vue'
const boardStore = useBoardStore()
const createBoard = ref(false)
getBoards()

defineOptions({
  name: 'IndexPage'
});

function getBoards() {
  const authStore = useAuthStore()
  if (authStore.isLoggedIn) {
    boardStore.getAll()
  }
}
</script>
