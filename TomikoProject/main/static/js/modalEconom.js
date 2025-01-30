function initModal() {
    const modal = document.getElementById('modal');
    const dialog = document.getElementById('overlayMenu');
    const closeBtn = modal.querySelector('.modal__close');
    const openBtn = document.querySelector('.hero__info-button--promo');
    
    function openModal() {
      modal.classList.add('active');
      dialog.show();
      document.body.classList.add('modal-open');
    }
    
    function closeModal() {
      modal.classList.remove('active');
      dialog.close();
      document.body.classList.remove('modal-open');
    }

    openBtn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });
    
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
      }
    });
  }
  document.addEventListener('DOMContentLoaded', initModal);