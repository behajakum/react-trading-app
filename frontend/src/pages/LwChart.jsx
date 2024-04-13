import CandlestickChart from "../components/CandlestickChart";
import localJsonData from '../../../../data/26000.json';
import { useState } from "react";
import IndicatorChart from "../components/IndicatorChart";

const LwChart = () => {
  const [started, setStarted] = useState(false);
  const handleClick = (event) => {
      setStarted(!started)
      event.target.style.color = started ? '' : 'salmon'
  }
  console.log( 'Started: '+ started.toString())

  const url = '/api/v1/alice/indicators/26000/1'  // TODO alice

  return ( 
      <>
        <button onClick = { handleClick }> 
            { started ? `Stop Updating` : `Start Updating` }
        </button>
        {/* <CandlestickChart url={url} started={ started }/>  */}
        <IndicatorChart url={url} started={ started }/> 
      </>
    );
}
 
export default LwChart;