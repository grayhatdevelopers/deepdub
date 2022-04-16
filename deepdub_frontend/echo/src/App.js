import { BrowserRouter ,Routes, Route} from "react-router-dom";

import Homescreen from "./pages/home_page";
import Echo from "./pages/echo_page";


function App() {
  return (
    <BrowserRouter>
    <Routes>
        <Route exact path="/" element={<Homescreen/>}/>
        <Route exact path="/echo_page" element={<Echo/>}/>
      </Routes>
      <div className="App">
        <Homescreen />
      </div>
    </BrowserRouter>
  );
}

export default App;
