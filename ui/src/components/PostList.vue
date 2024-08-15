<template>
  <div class="q-pa-md q-gutter-md">
    <q-list bordered class="rounded-borders">
      <q-item-label header>{{ route.params.category.name }}</q-item-label>

      <q-item clickable v-ripple v-for="post in postStore.posts" @click="postStore.navigate(route.params.board, route.params.category, post.id)">
        <q-item-section avatar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/avatar2.jpg">
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label lines="1">{{ post.name }}</q-item-label>
          <q-item-label caption lines="2">
            {{ post.content }}
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
import { useRouter, useRoute } from 'vue-router'
import { usePostStore } from 'src/stores/post';

const postStore = usePostStore()
const router = useRouter()
const route = useRoute()

</script>
