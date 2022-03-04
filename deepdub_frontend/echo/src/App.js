import logo from './logo.svg';
import './App.css';
import './recordButton.scss';

import RecordVideo from './webcamManager';


function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <img src={logo} className="App-logo" alt="logo" /> */}
        {/* <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a> */}
        {/* <h1 className="header">deepdub</h1> */}

        <RecordVideo />

      </header>
    </div>
  );
}

export default App;
