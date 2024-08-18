<template>
  <q-layout class="bg-grey-8 text-grey-4" view="hHh lpR fFf">

    <q-header bordered style="max-height:32px;" class="bg-deep-purple-8 text-grey-1">
      <q-toolbar style="min-height:0px">

        <q-toolbar-title style="font-size: 14px;">
          Chatterbox
        </q-toolbar-title>

        <div v-if="authStore.isLoggedIn">{{ authStore.user.name }}</div>
        <q-btn-dropdown dropdown-icon="account_circle" no-icon-animation flat dense round size="12px">
          <q-list>
            <q-item clickable v-close-popup @click="authStore.signOut()">
              <q-item-section>
                <q-item-label>Log out</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above class="bg-grey-9"  v-model="leftDrawerOpen" side="left">
      <CategoryList/>
      <!-- drawer content -->
    </q-drawer>

    <q-drawer show-if-above class="bg-grey-9" v-model="rightDrawerOpen" side="right">
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
import BoardIconList from 'src/components/BoardIconList.vue';
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
