import CandlestickChart from "../components/CandlestickChart";
import localJsonData from '../../../../data/26000.json';
import { useState } from "react";

const LwChart = () => {
  const [started, setStarted] = useState(false);
  const handleClick = (event) => {
      setStarted(!started)
      event.target.style.color = started ? '' : 'salmon'
  }
  console.log( 'Started: '+ started.toString())

  const url = '/api/v1/historical/26000/1'

  return ( 
      <>
        <button onClick = { handleClick }> 
            { started ? `Stop Updating` : `Start Updating` }
        </button>
        <CandlestickChart url={url} started={ started }/> 
      </>
    );
}
 
export default LwChart;