con=document.getElementById('container');
btn=document.getElementById('btn');
div=document.getElementsByClassName('fullbtn');
btn.addEventListener("click",function () {
  btn.style.display='none';
  con.style.display='block';
  document.onwebkitfullscreenchange = fullscreenChanged;
  document.documentElement.onclick= goFullscreen;
  document.onkeydown = goFullscreen;
  timer()
})
function goFullscreen() {
  // Must be called as a result of user interaction to work
  mf = document.documentElement
  mf.webkitRequestFullscreen();
  document.addEventListener("contextmenu", function(e){
    e.preventDefault();
  }, false);
  mf.style.display="";
}

function fullscreenChanged() {
  if (document.webkitFullscreenElement == null) {
    mf = document.documentElement;
    document.quizForm.submit()
    mf.style.display="none";
    
  }
}
function UpdateTimer() {
  var month = document.getElementById("month");
  var date = document.getElementById("date");
  var year = document.getElementById("year");

  var now = new Date();
  var mn = now.getMonth();
  var yr = now.getFullYear();
  var dt = now.getDate();

  var months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  month.innerHTML = months[mn];
  date.innerHTML = dt + ",";
  year.innerHTML = yr;
}

function timer() {
  UpdateTimer();
  var time = "00 : 01 : 20";
  var timeover = false;
  div=document.getElementById('timer')
  var tm = document.getElementById("time");
  tm.innerHTML = time;
  my_timer = setInterval(function () {
    var hr = 0,
      mt = 0,
      sc = 0;
    t = time.split(":");
    hr = parseInt(t[0]);
    mt = parseInt(t[1]);
    sc = parseInt(t[2]);

    if (sc == 0) {
      if (mt > 0) {
        sc = 59;
        mt--;
      } else if (hr > 0) {
        mt = 59;
        sc = 59;
        hr--;
      } else {
        timeover = true;
      }
    } else {
      sc--;
    }
    if(hr == 0 && mt == 0 && sc<=15){
      if(sc%2==0){
        div.style.background='red'
        div.style.color='White'
      }else{
        div.style.background='none'
        div.style.color='Black'

      }
    }
    if (mt < 10) {
      mt = "0" + mt;
    }
    if (hr < 10) {
      hr = "0" + hr;
    }
    if (sc < 10) {
      sc = "0" + sc;
    }
    time = hr + " : " + mt + " : " + sc;
    if (timeover) {
      tm = document.getElementById("time");
      tm.innerHTML = time;
      clearInterval(my_timer);
      /* forcefully submit form */
      document.quizForm.submit()
    } else {
      tm = document.getElementById("time");
      tm.innerHTML = time;
    }
  }, 1000);
}


