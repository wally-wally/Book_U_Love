import {
  loginUser,
  fetchMyInfo,
  updateMyInfo,
  deleteUser,
  changePassword,
  findPassword,
  fetchAllUsers } from '@/api/index.js'
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

const actions = {
  async LOGIN({ commit }, userData) {
    const result = await loginUser(userData)
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
    const { data } = await updateMyInfo(userData)
    return data
  },
  async CHANGE_PASSWORD({ getters }, userData) { // 유저의 비밀번호 변경을 요청하는 비동기 로직
    const { data } = await changePassword(userData, getters.info.user_id)
    return data
  },
  async DELETE_USER({ getters }) { // 회원탈퇴
    await deleteUser(getters.info.user_id)
  },
  async GET_MYBOOK_REVIEW_CNT({ getters }) {
    const { data } = await fetchMyInfo(getters.info.user_id)
    return data.review_set.length
  },
  async FIND_PASSWORD({ commit }, userData) {
    const data = await findPassword(userData)
    return data
  },
  async GET_ALL_USERS({ commit }, paramsData) {
    const { data } = await fetchAllUsers(paramsData)
    return data
  }
};

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
}
