import { RouterProvider, createBrowserRouter} from 'react-router-dom'
import RootLayout from './pages/RootLayout'
import ChartLayout from './pages/ChartLayout'
import LwChart from './pages/LwChart'

function App() {

  const router = createBrowserRouter([
    {
        path: '/',
        element: <RootLayout />,
        children: [
          { path: '/', element: <div>Home Page</div> },
        ]
    },
    {
      path: '/',
      element: <ChartLayout />,
      children: [
        { path: '/graph', element: <LwChart /> }
      ]
  }
  ])

  return (
    <>
      <RouterProvider router={ router } />
    </>
  )
}

export default App
