<template>
  <q-page>
    <div class="flex flex-center">
      <q-input v-model="authStore.signUpLogin.username" label="Username" />
      <q-input v-model="authStore.signUpLogin.password" type="password" label="Password" />
      <q-input v-model="authStore.signUpLogin.passwordConfirm" type="password" label="Confirm Password"/>
    </div>
    <div>
      <q-btn v-if="!register" label="Login"/>
      <q-btn v-if="!register" @click="register = true" label="Create Account"/>
      <q-btn v-if="register" label="Confirm"/>
      <q-btn v-if="register" @click="register = false" label="Back"/>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from 'src/stores/auth';

const authStore = useAuthStore()
const register = ref(false)
</script>
