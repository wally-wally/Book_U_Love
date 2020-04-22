import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store/index.js'
import { loadView, loadComponent } from '@/utils/loadPage.js'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '',
      name: 'MainPage',
      component: loadView('MainPage'),  // 메인 페이지
    },
    {
      path: '/login',
      component: loadView('LoginPage'),
      children: [
        { path: '', name: 'Login', component: loadComponent('Login', 'LoginForm'), beforeEnter: checkNoLoginUser },  // 로그인 페이지
        { path: '/signup', name: 'Signup', component: loadComponent('Login', 'SignUpToS'), beforeEnter: checkNoLoginUser },  // 로그인 페이지에서 회원가입 눌렀을 때 처음 나오는 이용약관 동의 페이지
        { path: '/signup/register', name: 'SignupForm', component: loadComponent('Login', 'SignUpForm'), beforeEnter: checkSignUpUser },  // 회원가입 Form(기본 정보 입력)
        { path: '/signup/success', name: 'SuccessSignup', component: loadComponent('Login', 'SuccessSignUp'), beforeEnter: checkAgreeToS },  // 회원가입 완료 후 페이지
      ],
    },
    {
      path: '/book',
      component: loadView('BookPage'),
      children: [
        { path: ':id', name: 'BookDetail', component: loadComponent('Books', 'BookDetail'), props: true } // 책 상세정보 페이지
      ]
    },
    {
      path: '/search/:query',
      name : "search",
      component: loadComponent('Books','BookSearch'),
    },
    {
      path: "/category",
      component: loadView('CategoryPage'),
      children: [
        { path: ':id', name: 'category', component:loadComponent('Books','Category'), props: true}
      ]
    },
    {
      path: '/myinfo',
      component: loadView('MyPage'),
      beforeEnter: checkLoginUser,
      children: [
        { path: '', name: 'MyPageMain', component: loadComponent('MyPage', 'MyPageMain') },
        { path: 'dashboard', name: 'MyDashBoard', component: loadComponent('MyPage', 'DashBoard') },
        { path: 'mybooks', name: 'MyBooks', component: loadComponent('MyPage', 'MyBooks') },
        { path: 'account', name: 'Account', component: loadComponent('MyPage', 'Account') }
      ]
    },
    {
      path: '/admin',
      name: 'AdminPage',
      component: loadView('AdminPage')
    },
    {
      path: '/collect',
      name: 'CollectData',
      component: loadComponent('Books', 'CollectReview')
    },
    {
      path: '*',
      name: 'NotFound',
      component: loadView('NotFoundPage'),  // 등록된 URL 주소가 아닌 곳으로 접근할 때 Not Found Page
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    if (to.hash) {
      return { selector: to.hash }
    }
    return { x: 0, y: 0 }
  }
})

function checkNoLoginUser(to, from, next) {  // 로그인이 안 된 경우에 로그인창, 회원가입창 접근 가능
  store.state.user.isLogin ? next('/') : next()
}

function checkLoginUser(to, from, next) {  // 로그인한 경우에만 My Page 접근 가능
  store.state.user.isLogin ? next() : next('/')
}

function checkSignUpUser(to, from, next) {
  store.state.user.agreeToS && from.name === 'Signup' && to.name === 'SignupForm' ? next() : next('/')
}

function checkAgreeToS(to, from, next) {
  store.state.user.agreeToS && from.name === 'SignupForm' && to.name === 'SuccessSignup' ? next() : next('/')
}