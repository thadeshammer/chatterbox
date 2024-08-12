<template>
  <q-page class="flex column">
    <div class="column">
      <q-input v-if="createBoard" v-model="boardStore.boardCreate.name" label="Name" />
      <q-input v-if="createBoard" v-model="boardStore.boardCreate.description" label="Description" />
      <q-btn v-if="!createBoard" @click="createBoard = !createBoard" label="Create Board"/>
      <q-btn v-if="createBoard" @click="boardStore.create(boardStore.boardCreate); createBoard = !createBoard" label="Confirm" />
    </div>

    <div class="column">
      <q-list bordered class="rounded-borders">
        <q-item-label header>Boards</q-item-label>

        <q-item clickable v-ripple v-for="board in boardStore.boards" @click="boardNav(board)">
          <q-item-section avatar>
            <q-avatar>
              <img src="https://cdn.quasar.dev/img/avatar2.jpg">
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label lines="1">{{ board.name }}</q-item-label>
            <q-item-label caption lines="2">
              {{ board.description }}
            </q-item-label>
          </q-item-section>

          <q-item-section side top>
            1 min ago
          </q-item-section>

          <q-separator inset="item" />
        </q-item>
      </q-list>
    </div>

  </q-page>
</template>

<script setup>
import { useBoardStore } from 'src/stores/board';
import { useCategoryStore } from 'src/stores/category';
import { useAuthStore } from 'src/stores/auth';
import { useRouter } from 'vue-router'
import { ref } from 'vue'
const boardStore = useBoardStore()
const categoryStore = useCategoryStore()
const router = useRouter()
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

async function boardNav(board) {
  await categoryStore.get(board)
  if (categoryStore.categories.length > 0) {
    var path = { path: '/board/' + board.name + '/category/' + categoryStore.categories[0].name }
    router.push(path)
  }
}
</script>
