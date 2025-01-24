      document.addEventListener('DOMContentLoaded', () => {
      const mainSwiper = new Swiper('.swiper-container', {
        slidesPerView: 3,
        mousewheel: false,
        spaceBetween: 16,
        navigation: {
          nextEl: '.custom-next',
          prevEl: '.custom-prev',
        },
    
      });
    
      const innerSwipers = document.querySelectorAll('.inner-slider');
    
      innerSwipers.forEach((swiperElement, swiperIndex) => {
        const swiperInstance = new Swiper(swiperElement, {
          spaceBetween: 0,
          centeredSlides: false,
          allowTouchMove: true,
          pagination: false,
          mousewheel: true,
          
        });
    
        const bullets = swiperElement.closest('.inner-slider__wrapper')
          .querySelectorAll('.inner-slider__pagination-bullet');
    
        bullets.forEach((bullet, index) => {
          bullet.addEventListener('click', () => {
            swiperInstance.slideTo(index);
    
            bullets.forEach(b => b.classList.remove('active'));
            bullet.classList.add('active');
          });
        });
    
        swiperInstance.on('slideChange', () => {
          bullets.forEach(b => b.classList.remove('active'));
          bullets[swiperInstance.activeIndex].classList.add('active');
        });
    
    
        bullets[0].classList.add('active');
      });
    });