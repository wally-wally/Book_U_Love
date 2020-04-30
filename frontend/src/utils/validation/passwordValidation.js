export function validatePassword(password) {
  var check_eng = /[a-z]/g; // 영어 소문자
  var check_num = /[0-9]/g; // 숫자
  var check_spc = /[!?@%]/g; // 특수문자
  if (password.match(check_eng) !== null && password.match(check_num) !== null && password.match(check_spc) !== null) {
    return password.match(check_eng).length >= 4 && password.match(check_num).length >= 2 && password.match(check_spc).length === 1
  }
}