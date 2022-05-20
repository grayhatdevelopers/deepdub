// import logo from "../logo.svg";
import "../App.css";
import "../recordButton.scss";
import RecordVideo from "../webcamManager";

import { SnackbarProvider } from "notistack";
import { React } from "react";

function Echo() {

  return (
    <SnackbarProvider maxSnack={3}>
      <div className="App">
        <header className="App-header">
          <RecordVideo />
        </header>
      </div>
    </SnackbarProvider>
  );
}

export default Echo;
