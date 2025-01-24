document.addEventListener('DOMContentLoaded', () => {
  const ttrack = document.querySelector(".lines__track");
  const sspeed = 1;
  let ooffset = 0;
  
  const cclone = ttrack.innerHTML; 
  ttrack.innerHTML += cclone;
  
  function aanimate() {
    ooffset -= sspeed;
    if (Math.abs(ooffset) >= ttrack.scrollWidth / 2) {
      ooffset = 0;
    }
    ttrack.style.transform = `translateX(${ooffset}px)`;
    requestAnimationFrame(aanimate);
  }
  
  aanimate();
  const linesTrack = document.querySelector(".lines__track--dark");
  const linesSpeed = 1; 
  let linesOffset = 0;
  
  const linesClone = linesTrack.innerHTML;
  linesTrack.innerHTML += linesClone;
  
  function animateLines() {
    linesOffset -= linesSpeed;  
    if (linesOffset <= -linesTrack.scrollWidth / 2) {
      linesOffset = 0;
    }
    linesTrack.style.transform = `translateX(${linesOffset}px)`;
    requestAnimationFrame(animateLines);
  }
  
  animateLines();
  
});