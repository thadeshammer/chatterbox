export default {
  urlEncode(inputString) {
    return inputString.replaceAll(" ", "-")
  },
  urlDecode(inputString) {
    return inputString.replaceAll("-", " ")
  }
}
