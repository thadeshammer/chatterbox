<template>
  <q-layout view="hHh lpR fFf">

    <q-header bordered class="bg-primary text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          Chatterbox
        </q-toolbar-title>

        <div v-if="authStore.isLoggedIn">{{ authStore.user.name }}</div>
        <q-btn-dropdown dropdown-icon="account_circle" no-icon-animation flat dense round size="24px">
          <q-list>
            <q-item clickable v-close-popup @click="authStore.signOut()">
              <q-item-section>
                <q-item-label>Log out</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
        <q-btn dense flat round icon="menu" @click="toggleRightDrawer" />
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
      <CategoryList/>
      <!-- drawer content -->
    </q-drawer>

    <q-drawer show-if-above v-model="rightDrawerOpen" side="right" bordered>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <div v-if="!authStore.isLoggedIn">
        <LoginPage/>
      </div>
      <div v-if="authStore.isLoggedIn">
        <router-view />
      </div>
    </q-page-container>

  </q-layout>
</template>


<script setup>
import { ref } from 'vue'
import CategoryList from 'src/components/CategoryList.vue';
import { useAuthStore } from 'src/stores/auth';
import { useBoardStore } from 'src/stores/board';
import LoginPage from 'src/pages/LoginPage.vue';

const leftDrawerOpen = ref(false)
const rightDrawerOpen = ref(false)
const board = useBoardStore()
function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}
function toggleRightDrawer() {
  rightDrawerOpen.value = !rightDrawerOpen.value
}

const authStore = useAuthStore();
board.init()
</script>
