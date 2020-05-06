import {
  fetchBooks,
  fetchBookDetail,
  fetchCategories,
  addBookReview,
  updateBookReview,
  fetchBookReview,
  recommend,
  postReviewLike} from '@/api/index.js'

const state = {
  categories: [],
  postReviewLoading: false,
  searchKeyword: '',
  detailCategories: [],
  mainBookTheme: 'All Books',
  allBooks: [],
  fetchAllBookStatus: false,
  allBooksCount: 0,
  nowBookCnt: 0
}

const mutations = {
  getCategoryList(state, categories) {
    state.categories = categories
  },
  getDetailCategoryList(state, categories) {
    let data = []
    for (const mainCategory of categories) {
      let mainCatsName = mainCategory.name
      for (const subCategory of mainCategory.subcategory_set) {
        let subCatsName = subCategory.name
        if (Object.prototype.hasOwnProperty.call(subCategory, 'detailcategory_set')) {
          for (const detailCategory of subCategory.detailcategory_set) {
            detailCategory['mainCatsName'] = mainCatsName
            detailCategory['subCatsName'] = subCatsName
            data.push(detailCategory)
          }
        }
      }
    }
    state.detailCategories = data
  },
  togglePostReviewLoading(state, status) {
    state.postReviewLoading = status
  },
  setSearchKeyword(state, keyword) {
    state.searchKeyword = keyword
  },
  toggleMainBookTheme(state, keyword) {
    state.mainBookTheme = keyword
  },
  storeAllBooks(state, books) {
    for (let i = 0; i < books.length; ++i) {
      state.allBooks.push(books[i])
    }
  },
  fetchAllBookStatus(state, status) {
    state.fetchAllBookStatus = status
  },
  allBooksCount(state, bookCnt) {
    state.allBooksCount = bookCnt
  },
  getNowCountBooks(state, count) {
    state.nowBookCnt = count
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
    await commit('getCategoryList', data.results)
    await commit('getDetailCategoryList', data.results)
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
  async EDIT_REVIEWS({ commit }, requestData) {
    const { data } = await updateBookReview(requestData)
    return data
  },
  async GET_RECOMMEND_BOOKS({ commit }) {
    const { data } = await recommend()
    return data
  },
  async POST_REVIEW_LIKE({ commit }, params) {
    const { data } = await postReviewLike(params)
    return data
  },
  async GET_RECOMMEND_OTHER_BOOKS({ commit }, params) {
    const { data } = await fetchBooks(params)
    return data
  }
}

const getters ={
  progressRate(state) {
    return ((state.nowBookCnt / state.allBooksCount) * 100).toFixed(0)
  }
}

export default {
  state,
  mutations,
  actions,
  getters
};
