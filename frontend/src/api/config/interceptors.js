import store from '@/store/index.js'

export function setInterceptors(instance) {
  instance.interceptors.request.use(
    config => {
      let token = store.state.user.token
      if (token) {
        config.headers['Authorization'] = 'JWT ' + store.state.user.token
      }
      return config
    },
    error => Promise.reject(error.response)
  )

  instance.interceptors.response.use(
    config => config,
    error => Promise.reject(error.response)
  )
  return instance
}