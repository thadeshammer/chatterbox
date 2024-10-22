const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: '/board/:board/category/:category/post/create', component: () => import('pages/CreatePostPage.vue')},
      { path: '/board/:board/category/:category', component: () => import('pages/CategoryPage.vue')},
      { path: '/board/:board/category/:category/post/:postId', component: () => import('pages/PostPage.vue')},
      { path: '/board/:board/admin', component: () => import ('pages/AdminPage.vue')}
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
