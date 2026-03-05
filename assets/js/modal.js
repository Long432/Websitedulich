function createModalMarkup() {
    if (document.getElementById('tour-modal-container')) return;
    const modalHTML = `
    <div id="tour-modal-container" class="tour-modal" onclick="closeTourModal(event)">
      <div class="tour-modal-content" onclick="event.stopPropagation()">
        <button class="tour-modal-close" onclick="closeTourModal(event)">&times;</button>
        <img id="tm-img" class="tour-modal-img" src="" alt="Hình ảnh">
        <div class="tour-modal-body">
          <h3 id="tm-title" class="tour-modal-title"></h3>
          <div class="tour-modal-highlight" id="tm-adv"></div>
          <p id="tm-desc" class="tour-modal-desc"></p>
          <div class="tour-modal-time">
            <i class="fas fa-clock"></i> <span id="tm-time"></span>
          </div>
        </div>
      </div>
    </div>
  `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

function openTourModal(element) {
    createModalMarkup();

    const title = element.getAttribute('data-title');
    const img = element.getAttribute('data-img');
    const desc = element.getAttribute('data-desc');
    const time = element.getAttribute('data-time');
    const adv = element.getAttribute('data-adv');

    document.getElementById('tm-title').textContent = title;
    document.getElementById('tm-img').src = img;
    document.getElementById('tm-desc').textContent = desc || 'Thông tin đang cập nhật...';
    document.getElementById('tm-time').textContent = time || 'Sáng hoặc chiều';

    const advEl = document.getElementById('tm-adv');
    if (adv) {
        advEl.textContent = adv;
        advEl.style.display = 'block';
    } else {
        advEl.style.display = 'none';
    }

    const modal = document.getElementById('tour-modal-container');
    // Trigger reflow
    modal.style.display = 'flex';
    setTimeout(() => modal.classList.add('show'), 10);

    // Prevent body scrolling
    document.body.style.overflow = 'hidden';
}

function closeTourModal(event) {
    if (event) event.stopPropagation();
    const modal = document.getElementById('tour-modal-container');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }, 300);
    }
}
