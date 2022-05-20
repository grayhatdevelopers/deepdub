import logo from './logo.svg';
import './App.css';

import { BrowserRouter ,Routes, Route} from "react-router-dom";

import Homescreen from "./pages/home_page";
import Echo from "./pages/echo_page";


function App() {
  return (
<SnackbarProvider maxSnack={3}>
  <div className="App">
    <BrowserRouter>
    <Routes>
        <Route exact path="/" element={<Homescreen/>}/>
        <Route exact path="/echo_page" element={<Echo/>}/>
      </Routes>
    </BrowserRouter>
  </div>
</SnackbarProvider>
  );
}

export default App;
