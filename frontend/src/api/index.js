import axios from "axios"
import { setInterceptors } from './config/interceptors'
import { _ } from "core-js"

// axios 초기화 함수
function createInstance() {
  const instance = axios.create({
    baseURL: 'http://i02b205.p.ssafy.io:8000/'
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

// 비밀번호 변경 API
function changePassword(userData, user_id) {
  return instance.put(`accounts/password_update/${user_id}/`, userData)
}

// MyPage의 Account 페이지에서 유저 추가정보 가져오는 API
function fetchMyInfo() {
  return instance.get('accounts/user/')
}

// MyPage의 Account 페이지에서 추가정보 입력 후 추가정보 변경 API
function updateMyInfo(userData) {
  return instance.put('accounts/user/', userData)
}

// 회원탈퇴
function deleteUser(userData) {
  return instance.delete('accounts/user/', userData)
}

// 비밀번호 찾기
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

// 리뷰 작성 API
function addBookReview(params) {
  return instance.post('api/review/', params);
}

// 리뷰 수정 API
function updateBookReview(data) {
  return instance.put(`api/review/${data[0]}/`, data[1])
}

// 리뷰 삭제 API
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
  return instance.get('api/likecategory')
}

function recommend() {
  return instance.get('accounts/user/recommend')
}

function fetchauthor(id){
  return instance.get(`api/author/${id}`)
}

function fetchcategoryfilter(params) {
  return instance.get('api/category/filter', {params:params} )
}

function fetchreviewcategory() {
  return instance.get('api/category/review/')
}

function fetchAllUsers(paramsData) {
  return instance.get('accounts/allusers/', { params: paramsData })
}

function postReviewLike(params) {
  return instance.post('api/review/like/', params)
}

function fetchweekly(){
  return instance.get('api/review_orderby_date')
}

function fetchReviewFilter(params) {
  return instance.get('api/review_filter', {params:params})
}

function filterCategoryBooks(params) {
  return instance.get('api/filter_by_score_and_count', params)
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
  updateBookReview,
  fetchjjim,
  deleteBookReview,
  mylike,
  myBookdata,
  recommend,
  fetchauthor,
  fetchreviewcategory,
  fetchcategoryfilter,
  fetchAllUsers,
  postReviewLike,
  fetchweekly,
  fetchReviewFilter,
  filterCategoryBooks
}