import { store } from 'quasar/wrappers'
import { createPinia } from 'pinia'
import { markRaw } from 'vue'
import { useRouter } from 'vue-router';
import { useCategoryStore } from './category';
/*
 * If not building with SSR mode, you can
 * directly export the Store instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Store instance.
 */

export default store((/* { ssrContext } */) => {
  const pinia = createPinia()

  // You can add Pinia plugins here
  // pinia.use(SomePiniaPlugin)
  pinia.use(({ store }) => {
    var router = useRouter()
    var categoryStore = useCategoryStore()
    store.$router = markRaw(router)
    store.categoryStore = markRaw(categoryStore)
  });

  return pinia
})
