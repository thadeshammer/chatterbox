<template>
  <div class="">
    <q-list class="rounded-borders">
      <q-item-label header>{{ route.params.category.name }}</q-item-label>

      <q-item
        class="q-pa-md"
        clickable
        v-ripple
        v-for="post in postStore.posts"
        @click="postStore.navigate(route.params.board, route.params.category, post.id)"
      >
        <q-item-section avatar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/avatar2.jpg">
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label class="text-h5 text-weight-medium" lines="1">{{ post.name }}</q-item-label>
          <q-item-label class="text-caption" lines="2">
            {{ post.content }}
          </q-item-label>
        </q-item-section>

        <q-item-section side top class="text-grey-5 column justify-around">
            {{ timeUtil.timeSince(post.created_at) }}
            <!--{{ 0 }}<q-icon name="comment"/>-->
        </q-item-section>

        <q-separator inset="item" />
      </q-item>
    </q-list>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { usePostStore } from 'src/stores/post';
import timeUtil from 'src/utilities/time-util';

const postStore = usePostStore()
const route = useRoute()

</script>
