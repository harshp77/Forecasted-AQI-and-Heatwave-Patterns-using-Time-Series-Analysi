import { useState } from 'react'
import reactLogo from './assets/react.svg'
import './App.css'
import Header from './components/Header'
import Home from './pages/Home'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App mx-20">
      <Header />
      <Home />
    </div>
  )
}

export default App
