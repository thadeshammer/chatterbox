export default {
  urlEncode(inputString) {
    return inputString.replace(" ", "-")
  },
  urlDecode(inputString) {
    return inputString.replace("-", " ")
  }
}
