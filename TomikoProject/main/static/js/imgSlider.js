document.addEventListener('DOMContentLoaded', () => {
    const mainImage = document.querySelector('.main-image');
    const thumbnails = document.querySelectorAll('.thumbnail');
    const prevBtn = document.querySelector('.slider-btn.prev');
    const nextBtn = document.querySelector('.slider-btn.next');
  
    let currentIndex = 0;

    const updateMainImage = (index) => {
      mainImage.src = thumbnails[index].src;
      thumbnails.forEach((thumbnail, i) => {
        thumbnail.classList.toggle('active', i === index);
      });
    };
  
    thumbnails.forEach((thumbnail, index) => {
      thumbnail.addEventListener('click', () => {
        currentIndex = index;
        updateMainImage(currentIndex);
      });
    });
  
    prevBtn.addEventListener('click', () => {
      currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
      updateMainImage(currentIndex);
    });
  
    nextBtn.addEventListener('click', () => {
      currentIndex = (currentIndex + 1) % thumbnails.length;
      updateMainImage(currentIndex);
    });
  
    updateMainImage(currentIndex);
  });
  