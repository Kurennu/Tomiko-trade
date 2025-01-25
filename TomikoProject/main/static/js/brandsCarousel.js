document.addEventListener('DOMContentLoaded', () => {
const track = document.querySelector(".brands__carousel-track");
const speed = 1;
let offset = 0;

const clone = track.innerHTML;
track.innerHTML += clone;

function animate() {
  offset -= speed;
  if (Math.abs(offset) >= track.scrollWidth / 2) {
    offset = 0;
  }
  track.style.transform = `translateX(${offset}px)`;
  requestAnimationFrame(animate);
}

animate();
});