<template>
  <q-page>
    <div class="flex flex-center column">
      <q-input v-model="authStore.signUpLogin.name" label="Username"/>
      <q-input v-if="register" v-model="authStore.signUpLogin.email" label="Email" />
      <q-input v-model="authStore.signUpLogin.password" type="password" label="Password" />
      <q-input v-if="register" v-model="authStore.signUpLogin.passwordConfirm" type="password" label="Confirm Password"/>
    </div>
    <div class="flex flex-center">
      <q-btn v-if="!register" @click="authStore.getByName(authStore.signUpLogin.name)" label="Login"/>
      <q-btn v-if="!register" @click="register = true" label="Create Account"/>
      <q-btn v-if="register" @click="register = false" label="Back"/>
      <q-btn v-if="register" @click="authStore.create(authStore.signUpLogin)" label="Confirm"/>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from 'src/stores/auth';

const authStore = useAuthStore()
const register = ref(false)
</script>
