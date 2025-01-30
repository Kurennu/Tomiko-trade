document.addEventListener('DOMContentLoaded', () => {
  const mainSwiper = new Swiper('.swiper-container', {
    slidesPerView: 3,
    spaceBetween: 16,
    navigation: {
      nextEl: '.custom-next',
      prevEl: '.custom-prev',
    },
    on: {
      slideChange: function () {
        // Убираем класс "large" у всех слайдов
        this.slides.forEach((slide) => {
          slide.classList.remove('swiper-slide--large');
          slide.classList.add('swiper-slide--small');
        });

        // Добавляем класс "large" активному слайду
        if (this.slides[this.activeIndex]) {
          this.slides[this.activeIndex].classList.remove('swiper-slide--small');
          this.slides[this.activeIndex].classList.add('swiper-slide--large');
        }
      },
    },
  });

  // Инициализация внутренних слайдеров
  const innerSwipers = document.querySelectorAll('.inner-slider');
  innerSwipers.forEach((swiperElement) => {
    new Swiper(swiperElement, {
      spaceBetween: 0,
      pagination: {
        el: '.inner-slider__pagination',
        clickable: true,
      },
    });
  });
});