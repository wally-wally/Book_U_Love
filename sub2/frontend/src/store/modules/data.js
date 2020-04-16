import { fetchBooks, fetchBookDetail, fetchCategories,addBookReview } from '@/api/index'
import { fetchBookReview } from '../../api';

const state = {
  categories: []
}

const mutations = {
  getCategoryList(state, categories) {
    state.categories = categories
  }
}

const actions = {
  async GET_BOOKS({ commit }, pageNm) {  // 전체 책 정보 가져오기
    const { data } = await fetchBooks(pageNm)
    return data
  },
  async GET_BOOK_DETAIL({ commit }, params) {  // id 값을 파라미터로 넘겨서 해당 책 정보 가져오기
    const { data } = await fetchBookDetail(params)
    return data
  },
  async GET_CATEGORIES({ commit }) {  // 전체 카테고리 정보 가져오기
    const { data } = await fetchCategories()
    commit('getCategoryList', data.results)
    return data
  },
  async GET_REVIEWS({ commit },id) {  // 전체 리뷰가져오기
    const { data } = await fetchBookReview(id)
    console.log(data)
    return data
  },

  async ADD_REVIEWS({commit}, params) {
    console.log(params.data)
    const { data } = await addBookReview(params.id,params.data)
    return data
  }
};

export default {
  state,
  mutations,
  actions
};
