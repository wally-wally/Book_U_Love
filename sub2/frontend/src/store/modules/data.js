//추후 데이터를 불러오는 과정에서 사용될 vuex 파일

// import api from "../../api";
import { fetchBooks, fetchBookDetail, fetchCategories,addBookReview } from '@/api/index'
import { fetchBookReview } from '../../api';

const state = {
  books: [],
  categories: []
}

const mutations = {
  getBooksList(state, books) {
    state.books = books
  },
  getCategoryList(state, categories) {
    state.categories = categories
  }
}

const actions = {
  async GET_BOOKS({ commit }, pageNm) {  // 전체 책 정보 가져오기
    const { data } = await fetchBooks(pageNm)
    commit('getBooksList', data.results)
    return data
  },
  async GET_BOOK_DETAIL({ commit }, params) {  // id 값을 파라미터로 넘겨서 해당 책 정보 가져오기
    const { data } = await fetchBookDetail(params)
    return data.results
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

  // 기존 작성된 스켈레톤 코드
  // async getStores({ commit }, params) {
  //   const append = params.append;
  //   const resp = await api.getStores(params);
  //   const stores = resp.data.results.map(d => ({
  //     id: d.id,
  //     name: d.store_name,
  //     branch: d.branch,
  //     area: d.area,
  //     tel: d.tel,
  //     address: d.address,
  //     lat: d.latitude,
  //     lng: d.longitude,
  //     categories: d.category_list
  //   }));

  //   if (append) {
  //     commit("addStoreSearchList", stores);
  //   } else {
  //     commit("setStoreSearchList", stores);
  //   }
  //   commit("setStoreSearchPage", resp.data.next);
  // }
};

export default {
  state,
  mutations,
  actions
};
