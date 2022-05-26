import {useEffect} from 'react';

import $ from "jquery";

import YouTube from 'react-youtube';


const MainPage = () => {

    const opts = {
        height: '100%',
        width: '100%',
        frameborder: "0",
        allow: "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture",
        playerVars: { 'autoplay': 1, 'controls': 1,'autohide':1,'wmode':'opaque' },
    }


    useEffect (() => {
        $('.signin').hover(function() {}, function() {
            $(this).addClass('animateout');
            setTimeout(function() {
              $('.signin').removeClass('animateout');
            }, 750);
          });
          
          $('.signin').on('click', function() {
            $('.overlay').toggleClass('active');
            $('signinform-field').removeClass('focus');
            $('input').val('');
            return false;
          });
          $('input').focus(function() {
            $(this).parent().addClass('focus');
          }).blur(function() {
            if ($(this).val() == '') {
              $(this).parent().removeClass('focus');
            }
            if ($('#fdEmail').val() != '' && $('#fdPassword').val() != '') {
              $('#btSubmit').addClass('active');
            } else {
              $('#btSubmit').removeClass('active');
          
            }
          });
          $('#btSubmit').on('click', function() {
            return false;
          });
          $('#btCancel').on('click', function() {
            $('.overlay').removeClass('active');
            return false;
          });
    })

    // The react-youtube API will call this function when the video player is ready.
    function onPlayerReady(event) {
        event.target.mute();
    }

    return (
    <div class="welcome-page">
<div class="overlay">
    <a href="#" class="signin">Sign In</a>
    <form class="signinform">
    <div class="signinform-field fadeIn">
      <label for="fdEmail">Email address</label>
      <input id="fdEmail" type="email" />
    </div>
    <div class="signinform-field fadeIn">
      <label for="fdPassword">Password</label>
      <input id="fdPassword" type="password" />
    </div>
    <div class="fadeIn">
      <button id="btSubmit" type="submit" class="signin-submit">Sign in</button>      <a href="https://www.twitter.com/mixchex" class="link-register">No password</a>

    </div>
    <div class="cancelarea fadeIn">
      <a href="#" class="cancelbtn" id="btCancel">Cancel</a>
  </div>
  </form>

<div class="overlay-svg">
<svg x="0px" y="0px"
	  viewBox="0 0 2000 1500" enable-background="new 0 0 2000 1500" >
<path opacity="0.8" fill="#221F1F" d="M0,0v1500h2000V0H0z M797.266,815.83c-8.414,1.479-16.974,1.92-25.832,3.1l-27.011-79.113
	v82.512c-8.413,0.885-16.088,2.064-24.059,3.246V674.427h22.437l30.7,85.758v-85.758h23.765V815.83z M885.533,698.043h-41.771
	v31.736c9.152,0,23.174-0.443,31.588-0.443v23.616c-10.481,0-22.731,0-31.588,0.443v35.129c13.875-0.885,27.75-2.068,41.771-2.51
	v22.73l-65.39,5.166V674.425h65.39V698.043z M973.357,698.044h-24.503V806.68c-7.971,0-15.94,0-23.615,0.295V698.043h-24.503
	v-23.618h72.621l-0.003,23.618L973.357,698.044z M1054.537,698.047h-42.806v30.111l0.001-0.001h32.325v23.615h-32.325v53.582
	h-23.175V674.429h65.979V698.047z M1133.063,810.076c-21.106-1.33-42.215-2.658-63.766-3.1V674.427h23.615v110.26l0.002,0.002
	c13.432,0.293,27.012,1.33,40.148,2.064V810.076z M1176.163,813.471c-7.675-0.885-15.647-1.328-23.174-1.771V674.427h23.174V813.471
	z M1279.635,674.429l-29.965,71.884l29.965,79.261c-8.859-1.18-17.712-2.805-26.57-4.279l-16.973-43.689l-17.268,40.148
	c-8.564-1.479-16.828-1.92-25.389-3.104l30.405-69.227l-27.454-70.997h25.388l15.499,39.707l16.531-39.707h25.831L1279.635,674.429z
	"/>
</svg>
  </div>
</div>
<div class="video-wrapper">
  {/* <div class="ResponsiveYTPlayer">
     <video id="video" src="https://www.youtube.com/embed/PLv1NQpeSuO2sh05xY7ze_zQCmU4OV5Ce2?autoplay=1&playlist=PLv1NQpeSuO2sh05xY7ze_zQCmU4OV5Ce2&enablejsapi=1&controls=0&disablekb=1&loop=1&mute=1&start=2&end=12" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></video>
  </div> */}
  <div class="ResponsiveYTPlayer">
  <YouTube 
//   containerClassName="ResponsiveYTPlayer" 
  videoId="1TYDNq2J-Dc" opts={opts} 
  onReady={onPlayerReady} 
  />
  </div>
</div>
</div>
)
}

export default MainPage;