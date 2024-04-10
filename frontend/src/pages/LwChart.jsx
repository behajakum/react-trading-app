import dataAlice from '../../../../data/26000.json';
import CandlestickChart from "../components/CandlestickChart";


function getCandleDataLocal() {
  let data = dataAlice.map(d => ({
    time: Date.parse(d.time)/1000,
    open: d.open,
    high: d.high,
    low: d.low,
    close: d.close,
    volume: d.volume
}))
  return data
}

const LwChart = () => {
  const data =  getCandleDataLocal()
  // console.log(data)

    return ( 
        <>
          <CandlestickChart data={ data } />
        </>
     );
}
 
export default LwChart;