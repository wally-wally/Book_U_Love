import axios from "axios"
import { setInterceptors } from './config/interceptors'
import { _ } from "core-js"

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

// 비밀번호 변경 API(구현예정)
function changePassword(userData) {
  return instance.post('요청주소', userData)
}

// MyPage의 Account 페이지에서 유저 추가정보 가져오는 API
function fetchMyInfo() {
  return instance.get(`accounts/user/`)
}

// MyPage의 Account 페이지에서 추가정보 입력 후 추가정보 변경 API
function updateMyInfo(userData) {
  return instance.put(`accounts/user/`, userData)
}

function deleteUser(userData) {
  return instance.delete('accounts/user/', userData)
}

function findPassword(userData) {
  return instance.post('accounts/find_password/', userData)
}

// 저장된 모든 책 데이터를 가져오는 API
function fetchBooks(params) {
  return instance.get('api/books', { params: params })
}

// 특정 책 데이터를 가져오는 API
function fetchBookDetail(id) {
  return instance.get(`api/book/${id}`)
}

// 특정 책 리뷰를 가져오는 API
function fetchBookReview(id) {
  return instance.get('api/review/'+id);
}

function addBookReview(params) {
  return instance.post('api/review/', params);
}

function deleteBookReview(review_id) {
  return instance.delete('api/review/'+ review_id + '/');
}

// 저장된 모든 카테고리 데이터를 가져오는 API
function fetchCategories() {
  return instance.get('api/category', { params: { limit: 70, offset: 0 } }, {})
}

function fetchjjim(params){
  return instance.post('api/like', params)
}

function mylike(params){
  return instance.get('api/mylike', params)
}

function myBookdata(){
  return instance.get(`api/likecategory`)
}

function recommend() {
  return instance.get(`accounts/user/recommend`)
}

function fetchauthor(id){
  return instance.get(`api/author/`+id)
}
export {
  registerUser,
  loginUser,
  changePassword,
  fetchMyInfo,
  updateMyInfo,
  deleteUser,
  findPassword,
  fetchBooks,
  fetchBookDetail,
  fetchCategories,
  fetchBookReview,
  addBookReview,
  fetchjjim,
  deleteBookReview,
  mylike,
  myBookdata,
  recommend,
  fetchauthor
}