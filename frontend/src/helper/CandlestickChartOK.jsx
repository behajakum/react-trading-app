import { useRef, useEffect, useState } from "react";
import { ColorType, createChart } from 'lightweight-charts'
import fetchOhlcvData from "./fetchData";


const CandlestickChart = (props) => {
    const url = props.url
    const started = props.started

    const [csSeries, setCsSeries] = useState(null)
    
    const chartContainerRef = useRef();
    const chartOptions = { 
        layout: { 
          textColor: 'black',
          background: {
            type: ColorType.Solid,
            color: 'white'             
          }
        },
        width: 1425,
        height: 760,
        localization: {
            locale: 'en-IN',
            timeFormatter: (time) => {
                const date = new Date(time * 1000)
                const dateFormatter = new Intl.DateTimeFormat(navigator.language, {
                    hour: 'numeric',
                    minute: 'numeric',
                    second: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    year: '2-digit',
                    
                })
                return dateFormatter.format(date)
            }
        },
        timeScale: {
          timeVisible: true,
          secondVisible: false,
          rightOffset: 10,
          tickMarkFormatter: (time, tickMarkType, locale) => {
            const date = new Date(time * 1000)
            switch (tickMarkType) {
                case 0:  //TickMarkType.Year
                    return date.FullYear()
                case 1:  //Month
                    const monthFormatter = new Intl.DateTimeFormat(locale, {
                        month: 'short'
                    })
                    return monthFormatter.format(date)
                case 2:  //DayOfMonth
                    return date.getDate()
                case 3:  // TickMarkType.Time
                    const timeFormatter = new Intl.DateTimeFormat(locale, {
                        hour: 'numeric',
                        minute: 'numeric',
                        hourCycle: 'h23'
                    })
                    return timeFormatter.format(date);
                case 4:  // TimeWithSeconds
                    const timeWithSecondsFormatter = new Intl.DateTimeFormat(locale, {
                        hour: 'numeric',
                        minute: 'numeric',
                        second: 'numeric'
                    })
                    return timeFormatter.format(date);
                default:
                    console.log('This tick format is not included')
            }
        }}
    };

    // Create chart
    useEffect(() => {
        const chart = createChart(chartContainerRef.current, chartOptions);

        const candlestickSeries = chart.addCandlestickSeries({
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderVisible: false,
            wickUpColor: '#26a69a',
            wickDownColor: '#ef5350'
        });

        // const fetchData = async () => {
        //     try {
        //         const initialData = await fetchOhlcvData(url)
        //         candlestickSeries.setData(initialData.slice(0, initialData.length - 3));
        //         setCsSeries(candlestickSeries)
        //     } catch (err) {
        //       console.error(err);
        //     }
        //   };
        // fetchData();

        (async () => {
            try {
                const initialData = await fetchOhlcvData(url)
                candlestickSeries.setData(initialData.slice(0, initialData.length - 3));
                setCsSeries(candlestickSeries)
            } catch (err) {
                console.error(err);
            }
        })()

        return () => {
            console.log('cleanup ran for rendered chart')
            chart.remove()
        }
    }, [])

    // Update chart
    useEffect(() => {
        let intervalId = null
        if (started) {
            intervalId = setInterval(() => {
            console.log(`setup interval ran: ${ intervalId }`)

            fetchOhlcvData(url)
                .then(d =>  d.slice(-1)[0])
                .then(d => {
                    csSeries.update(d)
                    console.log(d)
                })

          }, 20000)
        }
    
        return( () => {
          clearInterval(intervalId)
          console.log(`removed setup interval: ${ intervalId }`)
        })
      }, [started])

    return ( 
        <div ref= { chartContainerRef }></div>
     );
}
 
export default CandlestickChart;