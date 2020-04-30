export function validateUserName(username) {
  var check_num = /[0-9]/; // 숫자
  var check_eng = /[a-zA-Z]/; // 문자
  var check_spc = /[~!@#$%^&*()_+|<>?:{}]/; // 특수문자
  var check_kor = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/; // 한글체크
  // 한글로만 입력 가능
  return check_kor.test(username) && !check_num.test(username) && !check_eng.test(username) && !check_spc.test(username)
}