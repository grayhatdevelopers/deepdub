import DemoVideo from "../video.mp4";

function BackgroundVideo() {
    return <video autoPlay loop muted poster="https://assets.codepen.io/6093409/river.jpg"
      style={{
        position: "absolute",
        width: "100vw",
        top: "0",
        left: "0",
        right: "0",
        bottom: "0",
        height: "100vh",
        objectFit: "cover",
        zIndex: "-1",
//        opacity: "0.5",
      }}>
      <source src={DemoVideo} type="video/mp4" /> Your browser does not support the video tag. I suggest you upgrade your browser.
    </video>;
  }

export default BackgroundVideo;