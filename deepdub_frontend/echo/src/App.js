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
    <head>
      {/* <!--Import materialize.css--> */}
      <link type="text/css" rel="stylesheet" href="css/materialize.min.css"  media="screen,projection"/>
    </head>
  <div className="App">
    <BrowserRouter>
    <Routes>
        <Route exact path="/" element={<Homescreen/>}/>
        <Route exact path="/echo" element={<Echo/>}/>
      </Routes>
    </BrowserRouter>

    {/* <!--JavaScript at end of body for optimized loading--> */}
    <script type="text/javascript" src="js/materialize.min.js"></script>

  </div>
</SnackbarProvider>
  );
}

export default App;
