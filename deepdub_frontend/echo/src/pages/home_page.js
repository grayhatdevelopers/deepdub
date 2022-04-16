import React, { useRef } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import "../App.css";

import {  Button } from "@mui/material";
import { useNavigate, Router } from "react-router-dom";


function Homescreen() {
  const myref = useRef();
  const navigate = useNavigate();

  return (
      <div
        style={{
          height: "100vh",
          backgroundColor: "black",
        }}
        className="content-container"
      >
        <div className="text-1">deepdub</div>
        <a href="" className="watch-video-container">
          <FontAwesomeIcon icon="fab fa-youtube" />
          <div className="text-2">Watch Video</div>
        </a>
        <div
          style={{
            height: "10%",
          }}
        ></div>
        <div className="watch-video-container">
          <Button
            size="large"
            style={{
              height: "100px",
              width: "300px",
              backgroundColor: "#474747",
              color: "white",
              fontFamily: "Red Hat Display",
              fontSize: "200%",
              fontWeight: "bold",
            }}
            onClick={() => navigate("/echo_page")}
          >
            Echo
          </Button>
          <div
            style={{
              width: "20%",
            }}
          ></div>
          <Button
            size="large"
            style={{
              height: "100px",
              width: "300px",
              backgroundColor: "#474747",
              color: "white",
              fontFamily: "Red Hat Display",
              fontSize: "200%",
              fontWeight: "bold",
            }}
          >
            Showup
          </Button>
        </div>
      </div>
  );
}

export default Homescreen;
