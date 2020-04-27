import { loginUser, fetchMyInfo, updateMyInfo, deleteUser, changePassword, findPassword } from '@/api/index.js'
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
    state.isLoginError = false
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
    const result = await loginUser(userData)
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
    if (result.data.token) {
      commit('setToken', result.data.token)
    } else {
      commit('loginError')
    }
    return result
  },
  async GET_MYINFO({ getters }) { // 유저의 정보 불러오는 비동기 로직
    const { data } = await fetchMyInfo(getters.info.user_id)
    return data
  },
  async CHANGE_USER_INFO({ getters }, userData) { // 유저의 추가정보를 수정할 때 사용되는 비동기 로직
    const { data } = await updateMyInfo(userData, getters.info.user_id)
    return data
  },
  async CHANGE_PASSWORD({ getters }, userData) { // 유저의 비밀번호 변경을 요청하는 비동기 로직
    const { data } = await changePassword(userData, getters.info.user_id)
    return data
  },
  async DELETE_USER({ getters }) {
    await deleteUser(getters.info.user_id)
  },
  async GET_MYBOOK_REVIEW_CNT({ getters }) {
    const { data } = await fetchMyInfo(getters.info.user_id)
    return data.review_set.length
  },
  async FIND_PASSWORD({ commit }, userData) {
    await findPassword(userData)
  }
};

// getters
const getters = {
  info(state) {
    return state.token ? jwtDecode(state.token) : {}
  }
}

export default {
  state,
  mutations,
  actions,
  getters
};
