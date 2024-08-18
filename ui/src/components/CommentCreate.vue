<template>
  <q-input
    v-model="commentStore.createComment.content"
    filled
    type="textarea"
    label="Comment"
  />
  <div>
    <q-btn @click="commentStore.create()" label="Submit"/>
    <q-btn @click="commentStore.isCreateComment = false" label="Close"/>
  </div>
</template>
<script setup>
import { useCommentStore } from 'src/stores/comment';
const commentStore = useCommentStore()
</script>
