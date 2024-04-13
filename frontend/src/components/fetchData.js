export async function fetchAliceHistorical(url) {
    const res = await fetch(url)
    const data = await res.json()
    console.log(data)
    return data
}

export function convertToEpoch(timestampData) {
  const data = timestampData.map(d => ({
    time: Date.parse(d.time)/1000,
    open: d.open,
    high: d.high,
    low: d.low,
    close: d.close,
    volume: d.volume,
    EMA_9: d.EMA_9
  }))
  return data
}

async function fetchOhlcvData(url) {
    const candlesticks = await fetchAliceHistorical(url)
    // const candlesticks = convertToEpoch(timestampData);
    return candlesticks
}

export async function fetchInitialData(url) {
  const fromEpoch = Date.now() - 4 * 24 * 60 * 60 * 1000
  const toEpoch = Date.now()
  const fetchUrl = url + '?' + 'from_epoch' + '=' + fromEpoch + '&' + 'to_epoch' + '=' + toEpoch
  const candlesticks = await fetchAliceHistorical(fetchUrl)
  return candlesticks
}

export async function fetchUpdateData(url) {
  const fromEpoch = Date.now() - 24 * 60 * 60 * 1000
  const toEpoch = Date.now()
  let fetchUrl = url + '?' + 'from_epoch' + '=' + fromEpoch + '&' + 'to_epoch' + '=' + toEpoch
  const candlesticks = await fetchAliceHistorical(fetchUrl)
  console.log(fetchUrl)
  console.log(candlesticks)
  return candlesticks
}

export default fetchOhlcvData;