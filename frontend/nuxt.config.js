module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'staya-client',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'The web client for staya' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  css: [
    { src: '@/assets/main.scss', lang: 'sass' },
    { src: '@/node_modules/@mdi/font/scss/materialdesignicons.scss', lang: 'sass'}
  ],

  /*
  ** Customize the progress bar color
  */
  loading: { color: '#8854d0' },
  /*
  ** Build configuration
  */
  build: {
    /*
    ** Run ESLint on save
    */
    extend (config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        })
      }
    }
  },

  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/dotenv',
    '@nuxtjs/bulma',
    '@nuxtjs/pwa',
    '@nuxtjs/auth',
    '@nuxtjs/toast',
    'nuxt-buefy',
    'nuxt-validate'
  ],

  toast: {
    position: 'top-right',
    duration: 2000
  },

  axios: {
    baseURL: 'http://localhost:8000/api/v1'
  },

  auth: {
    strategies: {
      local: {
        endpoints: {
          login: { url: '/auth/login/', method: 'post', propertyName: 'key' },
          logout: false,
          user: { url: '/auth/user/', method: 'get', propertyName: false }
        },
        tokenRequired: true,
        tokenType: 'Token'
      }
    },
    redirect: {
      login: '/auth/login',
      logout: '/'
    }
  }
}
