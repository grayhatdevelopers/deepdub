import {useEffect, useState} from "react"

import { useRecordWebcam } from 'react-record-webcam'


import request from './utils/request';
import {baseUrl} from './utils/request';

import EchoTitle from './echoTitle';


import { axios, CancelToken } from "axios"

import ArrowForwardIcon from '@mui/icons-material/ArrowForward';



// Material UI for React
import { 
        FormControl, 
        InputLabel,
        Select,
        MenuItem, 
        CircularProgress,
        Button
    } from '@mui/material';

// for notifications
import { SnackbarProvider, useSnackbar } from 'notistack';


import Check from '@mui/icons-material/Check';

import {
	Replay,
	Download,
	} from '@mui/icons-material';



    import { borders } from '@mui/system';


    import { createTheme } from '@mui/material/styles';
    import { ThemeProvider } from '@mui/styles'; 
    

import { makeStyles } from '@mui/styles';

const buttonIconStyles = { 
    width: "120px", 
    height: "120px" 
}
const useStyles = makeStyles({
    button: {
        //margin: "20px",
        width: "150px",
        height: "150px",
    },
    root: {
      //width: 200,
      color: "white",
      borderColor: "white",
      outlineColor: "white",
    "& $notchedOutline": {
      borderColor: "red"
    },
    "&$focused $notchedOutline": {
        borderColor: "green"
    },
    '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
        borderColor: 'red',
    },      

    "& .MuiOutlinedInput-notchedOutline": {
        borderColor: "white"
    },
 
    "& .MuiOutlinedInput-notchedOutline .MuiSelect-icon": {
        color: "white"
    },
 
    
    "& .MuiOutlinedInput-notchedOutline:hover": {
      borderColor: "orange"
    },
    '.MuiOutlinedInput-notchedOutline': {
        borderColor: '#color',
      },
      '&:hover .MuiOutlinedInput-notchedOutline': {
        borderColor: '#color',
        borderWidth: '0.15rem',
      },


      "& .MuiOutlinedInput-input": {
        color: "white"
      },
      "& .MuiInputLabel-root": {
        color: "white"
      },
      "& .MuiOutlinedInput-root .MuiOutlinedInput-notchedOutline": {
        borderColor: "white"
      },
      "&:hover .MuiOutlinedInput-input": {
        color: "white"
      },
      "&:hover .MuiInputLabel-root": {
        color: "white"
      },
      "&:hover .MuiOutlinedInput-root .MuiOutlinedInput-notchedOutline": {
        borderColor: "white"
      },
      "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-input": {
        color: "white"
      },
      "& .MuiInputLabel-root.Mui-focused": {
        color: "white"
      },
      "& .MuiOutlinedInput-root.Mui-focused .MuiOutlinedInput-notchedOutline": {
        borderColor: "white"
      }
    },
  });


const styles = theme => ({
    select: {
        '&:before': {
            borderColor: "white",
        },
        '&:after': {
            borderColor: "white",
        }
    },
    icon: {
        fill: "white",
    },
});



// const theme = createTheme({
//   palette: {
//     primary: {
//       light: '#fff',
//       main: '#fff',
//       dark: '#fff',
//       contrastText: '#fff',
//     },
//     secondary: {
//       light: '#fff',
//       main: '#fff',
//       dark: '#fff',
//       contrastText: '#fff',
//     },
//   },
// });

const theme = createTheme({
    components: {
      // Name of the component
      MuiSelect: {
        styleOverrides: {
          // Name of the slot
          root: {
            // Some CSS
            fontSize: '1rem',
            borderColor: "white",
            '&:outlined':{
                borderColor: "white",
            }
          },
        },
      },
    },
})


const RecordVideo = (props) => {


	// for notifications
	  const { enqueueSnackbar } = useSnackbar();

const audio = new Audio("/record.mp3")

  const classes = useStyles()

  const recordWebcam = useRecordWebcam();

  const [response_file, setResponseFile] = useState(null);
  const [log_file, setLogFile] = useState(null);
  
  const [from, setFrom] = useState("German");
  const [to, setTo] = useState("English");


  const handleToInputChange = (event) => {
    // const target = event.target;
    const value = event.target.value;
    // const name = target.name;
    setTo(value);
  }

  const handleFromInputChange = (event) => {
    // const target = event.target;
    const value = event.target.value;
    // const name = target.name;
    setFrom(value);
  }

  const retakeVideo = (e) => {
    setResponseFile(null);
    recordWebcam.retake(e);
  }

  const startRecording = (e) => {
        // interrupts in recording...
        // audio.play()
    
        // animation starts... it should not start until the recordWebcam function starts
        // setTimeout(function() { recordWebcam.start(e); }, 2000);
        recordWebcam.start(e)
  }


  const [isProcessing, setProcessing] = useState(false)

  const saveFile = async () => {
    const blob = await recordWebcam.getRecording();
    // ...

    const data = new FormData();
    data.append('from_language', from);
    data.append('to_language', to);
    data.append('file', blob, blob.name);

    setProcessing(true)

    return request.post(`/uploadfile/`, data, {
      headers: {
        'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
      },
//      timeout: 30000,
    })
    .then( (res) => {
        console.log("response is:", res)
        console.log("filename is:", res.data.filename)
	setProcessing(false)
        setResponseFile(baseUrl + res.data.filename)
        enqueueSnackbar('Your video was processed successfully!', "success");
        setLogFile(baseUrl + res.data.logs)
    })
    .catch( (err) => {
    	setProcessing(false)
        enqueueSnackbar('['+ err.response.status +']'+' Failed to process your video. Reason: ' + err.response.data.message, "error");
        setLogFile(baseUrl + err.response.data.logs)
    });
};


useEffect( () => {
    recordWebcam.open()
}, [])


  return (
      <>
    <div style={{
        zIndex: 1, 
        position: "absolute",
        height: "100vh",
        width: "100vw",   
        transition: "1s ease-out",
        opacity: (recordWebcam.status == "RECORDING" || recordWebcam.status == "PREVIEW") ? 
                 1 : 0.4, 
    }}>
        <video ref={recordWebcam.previewRef} autoPlay controls style={{
            zIndex: 2, 
            position: "absolute",
            height: '100vh', 
            width: '100vw', 
            top: 0,
            left: 0,
            objectFit: "cover",
            visibility: recordWebcam.status == "PREVIEW" ?
            "visible" : "hidden"
        }}/>
        <video ref={recordWebcam.webcamRef} autoPlay muted style={{
            zIndex: 3, 
            position: "absolute",
          height: '100vh', 
          width: '100vw', 
          top: 0,
          left: 0,
          objectFit: "cover",
          visibility: recordWebcam.status == "PREVIEW" ?
                "hidden" : "visible" 
        }}/>

    </div>

<div style={{
        zIndex: 81,
        textAlign: 'center',
        verticalAlign: 'middle',
        transition: "0.5s",
    }}>

    { (recordWebcam.status == "RECORDING" || recordWebcam.status == "PREVIEW") ? <></> :

    <>
    {/* <h1 style={{
        fontSize: "140px",
        fontWeight: "bold",
        margin: "0px",
        marginTop: "-50px",
    }}>Echo</h1> */}
    <EchoTitle style={{marginTop: "-50px"}}/>
    <h3 style={{
        // fontSize: "140px",
        // fontWeight: "bold",
        marginTop: "10px",
        // marginTop: "10px",
        
    }}>See yourself speak in another language.</h3>

    <div style={{display:"flex", flexDirection: "row", alignItems:"center", justifyContent: "center", color: "white", verticalAlign: "center"}}>
    <ThemeProvider theme={theme}>

    <FormControl>

        <InputLabel style={{color:"white"}} id="demo-simple-select-label1">From</InputLabel>
        <Select
            // className={classes.select}
            
            className={classes.root}
            
            // inputProps={{
            //     classes: {
            //         icon: classes.icon,
            //         root: classes.root,
            //     },
            // }}

            // underlineStyle={{ borderColor: '#ff0000' }}
            // iconStyle={{ fill: '#ff0000' }}
            // labelStyle={{ color: '#ff0000' }}
            
            // sx={{ borderColor: 'white' }}

            labelId="demo-simple-select-label1"
            id="demo-simple-select1"
            value={from}
            label="From"
            onChange={handleFromInputChange}
        >
            <MenuItem value={"German"}>🇩🇪 German</MenuItem>
            <MenuItem value={"Urdu"}>🇵🇰 Urdu</MenuItem>
            <MenuItem value={"Hindi"}>🇮🇳 Hindi</MenuItem>
            <MenuItem value={"Chinese"}>🇨🇳 Chinese</MenuItem>            
        </Select>
    </FormControl>

    <ArrowForwardIcon style={{margin: "0px 40px 0px 40px"}}/>

    <FormControl>
        <InputLabel style={{color:"white"}} id="demo-simple-select-label2">To</InputLabel>
        <Select
            // className={classes.select}

            className={classes.root}

            // inputProps={{
            //     classes: {
            //         icon: classes.icon,
            //         root: classes.root,
            //     },
            // }}

            // underlineStyle={{ borderColor: '#ff0000' }}
            // iconStyle={{ fill: '#ff0000' }}
            // labelStyle={{ color: '#ff0000' }}

            // sx={{ borderColor: 'primary.main' }}
 

            labelId="demo-simple-select-label2"
            id="demo-simple-select2"
            value={to}
            label="To"
            onChange={handleToInputChange}
        >
            <MenuItem value={"English"}>🇬🇧 English</MenuItem>
        </Select>
    </FormControl>
    </ThemeProvider>
    </div>
</>
}
    
    {/* Possible operations of Recording */}
    
    {/* <p style={{marginBottom: "50px"}}>Camera status: {recordWebcam.status}</p>
    <div style={{
        marginBottom: "50px"
    }}>
      <button onClick={recordWebcam.open}>Open camera</button>
      <button onClick={recordWebcam.start}>Start recording</button>
      <button onClick={recordWebcam.stop}>Stop recording</button>
      <button onClick={recordWebcam.retake}>Retake recording</button>
      <button onClick={recordWebcam.download}>Download recording</button>
      <button onClick={saveFile}>Save file to server</button>
    </div> */}

      {/* <video ref={recordWebcam.previewRef} autoPlay muted loop /> */}

{/* 
    <div style={{
        position: "relative",
        marginTop: "40px",
    }}>

        <div id='c'>
        <div className="s"></div>
        </div>
        <div id='o'>
            <div className='o2' onClick={recordWebcam.status == "RECORDING" ? recordWebcam.stop : recordWebcam.start}></div>
        </div>
    </div>
 */}


{
    recordWebcam.status == "INIT" ?    
    <p style={{
        marginTop: "40px",
        opacity: 0.8,
        backgroundColor: "#00000054",
        // color: "",
        borderRadius: "50px",
        width: "auto",
        padding: "10px 5px 10px 5px",
    }}>Waiting for camera to connect...</p>
    :

    recordWebcam.status == "PREVIEW" ?

	<div style={{display:"flex", flexDirection:"column", alignItems:"center"}}>
<div style={{
        marginTop: "50px"
    }}>
      <Button size="large" className={classes.button} onClick={retakeVideo}>
        <Replay style={buttonIconStyles}/>
      </Button>
      <Button size="large" className={classes.button} onClick={recordWebcam.download}>
        <Download style={buttonIconStyles}/>
      </Button>      
    </div>     
    <div>
      <Button size="large" variant={response_file ? "outlined" : "contained"} className={classes.button} color="primary" onClick={saveFile} disabled={isProcessing}>
        { isProcessing ? <CircularProgress style={buttonIconStyles}/> : <Check style={buttonIconStyles}/> }
      </Button>
    </div>

      {response_file ? <Button size="large" variant="contained" href={response_file} target="_blank" style={{marginTop:"20px"}} >SEE YOUR RESULTS</Button> : <></>}
      {log_file ? <Button size="large" variant="outlined" href={log_file} target="_blank" style={{marginTop:"20px"}} >SEE LOG FILE</Button> : <></>}
    
    </div>
    
    :
        <div className="container" 
        style={{
            position: "relative",
            marginTop: "40px",
        }}>
            <input type="checkbox"
                onClick={recordWebcam.status == "RECORDING" ? recordWebcam.stop : startRecording} 
                id="btn"/>
            <label for="btn"></label>
            <div className="time">
                <div className="h_m"></div>
                <div style={{
                    marginLeft: "2px",
                }} className="s_ms"></div>
            </div>
        </div>
}


    
    </div>
    </>
  )
}

export default RecordVideo;
