export async function fetchAliceHistorical(url) {
    const res = await fetch(url)
    const data = await res.json()
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
    const timestampData = await fetchAliceHistorical(url)
    const candlesticks = convertToEpoch(timestampData);
    return candlesticks
}

export default fetchOhlcvData;