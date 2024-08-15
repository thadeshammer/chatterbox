<template>
  <q-page>
    <div v-if="postStore.selectedPost" class="column">
      <div class="text-h3">{{ postStore.selectedPost.name }}</div>
      <div>{{ postStore.selectedPost.content }}</div>
      <q-btn @click="isComment = true" v-if="!isComment" label="Leave a Comment"/>
      <q-input v-if="isComment" v-model="commentStore.createComment.content" label="Comment"/>
      <div v-if="isComment">
        <q-btn @click="commentStore.create(); isComment = false" label="Submit"/>
        <q-btn @click="isComment = false" label="Back"/>
      </div>

      <q-list bordered class="rounded-borders">
      <q-item-label header>Comments</q-item-label>

      <q-item clickable v-ripple v-for="comment in commentStore.comments">
        <q-item-section avatar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/avatar2.jpg">
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label caption lines="2">
            {{ comment.content }}
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
import { useRoute } from 'vue-router'
import { usePostStore } from 'src/stores/post';
import { useCategoryStore } from 'src/stores/category';
import { useBoardStore } from 'src/stores/board';
import { useCommentStore } from 'src/stores/comment'
import { ref, onBeforeMount } from 'vue'
import urlUtil from 'src/utilities/url-util';

const route = useRoute()
const postStore = usePostStore()
const categoryStore = useCategoryStore()
const boardStore = useBoardStore()
const commentStore = useCommentStore()
const isComment = ref(false)
postStore.selectById(route.params.postId)
if (!postStore.selectedPost) {
  onBeforeMount( async () => {
      await init(postStore.selectedPost)
    })
  }

  async function init(post) {
    if (!post) {
      await boardStore.getAll()
      var board = boardStore.getByName(urlUtil.urlDecode(route.params.board))
      await categoryStore.get(board)
      var category = categoryStore.getByName(urlUtil.urlDecode(route.params.category))
      await postStore.get(category)
      postStore.selectById(route.params.postId)
      await commentStore.getByPostId(postStore.selectedPost.id)
  }

}
</script>
