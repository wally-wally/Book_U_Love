import { fetchBooks, fetchBookDetail, fetchCategories, addBookReview, fetchBookReview } from '@/api/index.js'

const state = {
  categories: [],
  postReviewLoading: false
}

const mutations = {
  getCategoryList(state, categories) {
    state.categories = categories
  },
  togglePostReviewLoading(state, status) {
    state.postReviewLoading = status
  }
}

const actions = {
  async GET_BOOKS({ commit }, params) {  // 전체 책 정보 가져오기
    const { data } = await fetchBooks(params)
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
    return data
  },
  async ADD_REVIEWS({commit}, params) {
    const { data } = await addBookReview(params)
    return data
  },
};

export default {
  state,
  mutations,
  actions
};
