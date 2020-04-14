import axios from "axios"
import { setInterceptors } from './config/interceptors'

// axios 초기화 함수
function createInstance() {
  const instance = axios.create({
    baseURL: 'http://localhost:8000/' // [필수!!] 추후 배포된 주소로 변경
  })
  return setInterceptors(instance)
}
const instance = createInstance()

// 회원가입 API
function registerUser(userData) {
  return instance.post('accounts/signup/', userData)
}

// 로그인 API
function loginUser(userData) {
  return instance.post('accounts/auth-login/', userData)
}

// 비밀번호 확인 API(구현예정)
function checkPassword(password) {
  return instance.post('요청주소', password)
}

// 비밀번호 변경 API(구현예정)
function changePassword(password) {
  return instance.post('요청주소', password)
}

// MyPage의 Account 페이지에서 추가정보 입력 후 추가정보 변경 API(구현예정)
function updateMyInfo(userData) {
  return instance.post('요청주소', userData)
}

// 저장된 모든 책 데이터를 가져오는 API
function fetchBooks(pageNm) {
  return instance.get('api/books', { params: { page: pageNm } })
}

// 특정 책 데이터를 가져오는 API
function fetchBookDetail(params) {
  return instance.get('api/books', { params: params }, {})
}

// 특정 책 리뷰를 가져오는 API
function fetchBookReview(id) {
  return instance.get('api/review/'+id);
}

function addBookReview(id,params) {
  return instance.post('api/review/'+id + '/', params);
}

// 저장된 모든 카테고리 데이터를 가져오는 API
function fetchCategories() {
  return instance.get('api/category', { params: { limit: 70, offset: 0 } }, {})
}

export { registerUser, loginUser, checkPassword, changePassword, updateMyInfo, fetchBooks, fetchBookDetail, fetchCategories,fetchBookReview ,addBookReview}

