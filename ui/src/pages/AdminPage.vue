<template>
 <q-page>
  <q-list>
    <q-item-label header class="text-grey-4">Categories</q-item-label>
    <q-btn v-if="!isCreateCategory" @click="isCreateCategory = true" label="Add Category"/>
    <q-input v-if="isCreateCategory" v-model="cs.categoryCreate.name" label="Name"/>
    <q-input v-if="isCreateCategory" v-model="cs.categoryCreate.description" label="Description"/>
    <q-btn v-if="isCreateCategory" @click="isCreateCategory = false" label="Cancel"/>
    <q-btn v-if="isCreateCategory" @click="cs.create();isCreateCategory = false" label="Submit"/>
    <q-item bordered v-for="category in cs.categories">
      <q-item-section>
        <q-item-label lines="1">{{ category.name }}</q-item-label>
      </q-item-section>

      <q-item-section avatar>
        <q-btn flat round dense icon="delete"/>
      </q-item-section>
    </q-item>
  </q-list>
 </q-page>
</template>
<script setup>
import { useCategoryStore } from 'src/stores/category';
import { useBoardStore } from 'src/stores/board';
import { ref } from 'vue';
const cs = useCategoryStore()
const bs = useBoardStore()
cs.get(bs.getFromRoute())

const isCreateCategory = ref(false)
</script>
