import { useRef, useEffect, useState } from "react";
import { ColorType, createChart } from 'lightweight-charts'
import fetchOhlcvData, { fetchInitialData, fetchUpdateData } from "./fetchData";


const IndicatorChart = (props) => {
    const { url, started } = props

    const [csSeries, setCsSeries] = useState(null)
    const [emaFastSeries, setEmaFastSeries] = useState(null)
    const [emaSlowSeries, setEmaSlowSeries] = useState(null)
    const chartContainerRef = useRef();
    let refCount = useRef(0)
    
    const chartOptions = { 
        layout: { 
          textColor: 'black',
          background: {
            type: ColorType.Solid,
            color: 'white'             
          }
        },
        width: 1425,
        height: 740,
        // localization: {
        //     locale: 'en-IN',
        //     timeFormatter: (time) => {
        //         const date = new Date(time * 1000)
        //         const dateFormatter = new Intl.DateTimeFormat(navigator.language, {
        //             hour: 'numeric',
        //             minute: 'numeric',
        //             second: 'numeric',
        //             month: 'short',
        //             day: 'numeric',
        //             year: '2-digit',
                    
        //         })
        //         return dateFormatter.format(date)
        //     }
        // },
        // timeScale: {
        //   timeVisible: true,
        //   secondVisible: false,
        //   rightOffset: 10,
        //   tickMarkFormatter: (time, tickMarkType, locale) => {
        //     const date = new Date(time * 1000)
        //     switch (tickMarkType) {
        //         case 0:  //TickMarkType.Year
        //             return date.FullYear()
        //         case 1:  //Month
        //             const monthFormatter = new Intl.DateTimeFormat(locale, {
        //                 month: 'short'
        //             })
        //             return monthFormatter.format(date)
        //         case 2:  //DayOfMonth
        //             return date.getDate()
        //         case 3:  // TickMarkType.Time
        //             const timeFormatter = new Intl.DateTimeFormat(locale, {
        //                 hour: 'numeric',
        //                 minute: 'numeric',
        //                 hourCycle: 'h23'
        //             })
        //             return timeFormatter.format(date);
        //         case 4:  // TimeWithSeconds
        //             const timeWithSecondsFormatter = new Intl.DateTimeFormat(locale, {
        //                 hour: 'numeric',
        //                 minute: 'numeric',
        //                 second: 'numeric'
        //             })
        //             return timeFormatter.format(date);
        //         default:
        //             console.log('This tick format is not included')
        //     }
        // }}
    };

    // Create chart
    useEffect(() => {
        const chart = createChart(chartContainerRef.current, chartOptions);
        
        chart.applyOptions({
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
            }
        })
        
        chart.timeScale().applyOptions({
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
                }
            })

        // Candlestick
        const candlestickSeries = chart.addCandlestickSeries({
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderVisible: false,
            wickUpColor: '#26a69a',
            wickDownColor: '#ef5350'
        });
        
        // emas
        const emaFastLineSeries = chart.addLineSeries({ 
            color: 'red',
             lineWidth: 2 
        });  // ; to be tehre before async

        const emaSlowLineSeries = chart.addLineSeries({ 
            color: 'green',
             lineWidth: 2 
        });  
  
        (async () => {
            try {
                const initialData = await fetchOhlcvData(url)
                // const initialData = await fetchInitialData(url)
                // candlestickSeries.setData(initialData.slice(0, initialData.length - 10));  //TODO
                console.log(initialData)
                candlestickSeries.setData(initialData); 
                setCsSeries(candlestickSeries)

                const emaFastData = initialData
                    .filter(d => d.EMA_9)
                    .map(d => ({time: d.time, value: d.EMA_9}))
                emaFastLineSeries.setData(emaFastData)
                // emaFastLineSeries.setData(emaFastData.slice(0, emaFastData.length - 10))
                setEmaFastSeries(emaFastLineSeries)

                const emaSlowData = initialData
                    .filter(d => d.EMA_21)
                    .map(d => ({time: d.time, value: d.EMA_21}))
                emaSlowLineSeries.setData(emaSlowData)
                // emaSlowLineSeries.setData(emaSlowData.slice(0, emaSlowData.length - 10))
                setEmaSlowSeries(emaSlowLineSeries)

            } catch (err) {
                console.error(err)
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
                refCount.current = refCount.current + 1  // TODO for testing
                console.log(`setup interval ran: ${ intervalId }, ${refCount.current}`)
                // fetchOhlcvData(url)
                fetchUpdateData(url)
                    // .then(d =>  d.slice(-(11-refCount.current))[0])  // TODO simulation
                    .then(d =>  d.slice(-1)[0])  // TODO simulation
                    .then(d => {
                        console.log(d)
                        csSeries.update(d)
                        emaFastSeries.update({time: d.time, value: d.EMA_9})
                        emaSlowSeries.update({time: d.time, value: d.EMA_21})
                    })
                    .catch(err=>console.error(err))
          }, 30000)
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
 
export default IndicatorChart;