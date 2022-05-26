import DemoVideo from "../video.mp4";

import { useEffect } from 'react';

function BackgroundVideo({watchVideo}) {
    

//   useEffect( () => {
//     /* Store the element in el */
// let el = document.getElementById('tilt')

// console.log("Got the tilt element:" , el)

// /* Get the height and width of the element */
// const height = el.clientHeight
// const width = el.clientWidth

// /*
//   * Add a listener for mousemove event
//   * Which will trigger function 'handleMove'
//   * On mousemove
//   */
// el.addEventListener('mousemove', handleMove)

// /* Define function a */
// function handleMove(e) {
//   /*
//     * Get position of mouse cursor
//     * With respect to the element
//     * On mouseover
//     */
//   /* Store the x position */
//   const xVal = e.layerX
//   /* Store the y position */
//   const yVal = e.layerY
  
//   /*
//     * Calculate rotation valuee along the Y-axis
//     * Here the multiplier 20 is to
//     * Control the rotation
//     * You can change the value and see the results
//     */
//   const yRotation = 20 * ((xVal - width / 2) / width)
  
//   /* Calculate the rotation along the X-axis */
//   const xRotation = -20 * ((yVal - height / 2) / height)
  
//   /* Generate string for CSS transform property */
//   const string = 'perspective(500px) scale(1.1) rotateX(' + xRotation + 'deg) rotateY(' + yRotation + 'deg)'
  
//   /* Apply the calculated transformation */
//   el.style.transform = string
// }

// /* Add listener for mouseout event, remove the rotation */
// el.addEventListener('mouseout', function() {
//   el.style.transform = 'perspective(500px) scale(1) rotateX(0) rotateY(0)'
// })

// /* Add listener for mousedown event, to simulate click */
// el.addEventListener('mousedown', function() {
//   el.style.transform = 'perspective(500px) scale(0.9) rotateX(0) rotateY(0)'
// })

// /* Add listener for mouseup, simulate release of mouse click */
// el.addEventListener('mouseup', function() {
//   el.style.transform = 'perspective(500px) scale(1.1) rotateX(0) rotateY(0)'
// })
//   })


    if (!watchVideo){
    return <video 
    // id="tilt"
    
    autoPlay loop muted 
    // poster="https://assets.codepen.io/6093409/river.jpg"
      style={{
        // position: "absolute",
        width: "100vw",
        // top: "0",
        // left: "0",
        // right: "0",
        // bottom: "0",
        height: "100vh",
        objectFit: "cover",
        zIndex: "-1",
//        opacity: "0.5",
      }}>
      <source src={DemoVideo} type="video/mp4" /> Your browser does not support the video tag. I suggest you upgrade your browser.
    </video>;
    }
    else {
        return <video autoPlay loop 
        // poster="https://assets.codepen.io/6093409/river.jpg"
      style={{
        // position: "absolute",
        width: "100vw",
        // top: "0",
        // left: "0",
        // right: "0",
        // bottom: "0",
        height: "100vh",
        objectFit: "cover",
        zIndex: "-1",
//        opacity: "0.5",
      }}>
      <source src={DemoVideo} type="video/mp4" /> Your browser does not support the video tag. I suggest you upgrade your browser.
    </video>;
    }
  }

export default BackgroundVideo;
