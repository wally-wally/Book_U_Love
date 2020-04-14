import { loginUser } from '@/api/index.js'
import jwtDecode from 'jwt-decode'

const state = {
  adminAuth: 0,
  token: sessionStorage.getItem('token'),
  isLogin: sessionStorage.getItem('token') === null ? false : true,
  isLoginError: false,
  agreeToS: false
};

const mutations = {
  setToken(state, token) {
    state.token = token
    sessionStorage.setItem('token', token)
    state.isLogin = true
  },
  logout(state) {
    state.token = ''
    state.isLogin = false
    state.isLoginError = false
    state.agreeToS = false
    sessionStorage.clear()
  },
  loginError(state) {
    state.isLoginError = true
  },
  changeToS(state, check) {
    state.agreeToS = check
  }
}

// actions
const actions = {
  async LOGIN({ commit }, userData) {
    const { data } = await loginUser(userData)
    // 백엔드에서 프론트엔드로 보내는 data에 담겨야 하는 정보
    // (1) E-mail와 Password가 일치하게 잘 작성했는지 여부(=== 로그인 성공/실패 여부)(로그인 실패한 경우 token = null이나 empty string으로 받음)
    // (2) 아래와 같은 형태로 token 제공(가정)
    // data: {
    //   token: '~~~'
    // }
    //////////////////////////////
    // (3) jwtDecode로 token 값 풀었을 때 들어있는 유저 정보 형태(가정)
    // userdata: {
    //   adminAuth: 1 또는 0,  1인 경우 관리자 계정, 0은 일반 유저 계정 표시
    //   username: '~~',
    //   email: '~~',
    //   gender: '~~',
    //   age: '~~',
    //   ...
    // }
    if (data.token) {
      commit('setToken', data.token)
    } else {
      commit('loginError')
    }
  }
};

// getters
const getters = {
  // adminAuth(state) {
  //   return state.token ? jwtDecode(state.token).userData.adminAuth : 0
  // },
  userName(state) {
    return state.token ? jwtDecode(state.token).username : ''
  },
  userEmail(state) {
    return state.token ? jwtDecode(state.token).email : ''
  },
  // userGender(state) {
  //   return state.token ? jwtDecode(state.token).userData.userGender : ''
  // },
  // userAge(state) {
  //   return state.token ? jwtDecode(state.token).userData.age : ''
  // },
}

export default {
  state,
  mutations,
  actions,
  getters
};
