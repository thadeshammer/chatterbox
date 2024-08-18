<template>
  <div v-html="result"></div>
</template>
<script setup>
import markdownit from 'markdown-it'
const md = markdownit()
const props = defineProps({
  content: {
    type: String,
    required: true
  }})
const result = md.render(props.content);
console.log(result)
</script>
