
const url = '/api/v1/local/indicators/26000/1'

const fromEpoch = Date.now() - 1 * 60 * 60 * 1000
const toEpoch = Date.now()

const updateUrl = url + '?' + 'fromEpoch' + '=' + fromEpoch + '&' + 'toEpoch' + '=' + toEpoch

console.log(fromEpoch)
console.log(updateUrl)
console.log(toEpoch)