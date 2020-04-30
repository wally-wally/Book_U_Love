export function validateNumber(num) {
  var check_num = /[0-9]/; // 숫자
  return check_num.test(num)
}