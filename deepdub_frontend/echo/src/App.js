import logo from './logo.svg';
import './App.css';

import { BrowserRouter ,Routes, Route} from "react-router-dom";

import Homescreen from "./pages/home_page";
import Echo from "./pages/echo_page";


// for notifications
import { SnackbarProvider, } from 'notistack';

function App() {
  return (
<SnackbarProvider maxSnack={3}>
  <div className="App">
    <BrowserRouter>
    <Routes>
        <Route exact path="/" element={<Homescreen/>}/>
        <Route exact path="/echo" element={<Echo/>}/>
      </Routes>
    </BrowserRouter>
  </div>
</SnackbarProvider>
  );
}

export default App;
