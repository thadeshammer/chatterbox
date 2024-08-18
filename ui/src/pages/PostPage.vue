<template>
  <q-page>
    <div v-if="postStore.selectedPost" class="column">
      <div class="text-h3">{{ postStore.selectedPost.name }}</div>
      <Markdown :content="postStore.selectedPost.content"/>
      <div>
        <q-space/>
        <q-btn @click="commentStore.isCreateComment = true" v-if="!commentStore.isCreateComment" label="Leave a Comment"/>
      </div>
      <CommentCreate v-if="commentStore.isCreateComment"/>
    </div>
    <q-list>
      <q-card class="bg-grey-7" flat v-for="comment in commentStore.comments">
        <q-card-section>
          {{ comment.content }}
        </q-card-section>
        <q-card-actions>
          <q-btn flat>Reply</q-btn>
          <q-btn flat>View Replies (2)</q-btn>
        </q-card-actions>
      </q-card>
    </q-list>
  </q-page>
</template>
<script setup>
import { useRoute } from 'vue-router'
import { usePostStore } from 'src/stores/post';
import { useCategoryStore } from 'src/stores/category';
import { useBoardStore } from 'src/stores/board';
import { useCommentStore } from 'src/stores/comment'
import { ref, onBeforeMount } from 'vue'
import Markdown from 'src/components/Markdown.vue';
import urlUtil from 'src/utilities/url-util';
import CommentCreate from 'src/components/CommentCreate.vue';

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
