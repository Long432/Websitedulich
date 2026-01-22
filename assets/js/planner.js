// --- 1. KHỞI TẠO DỮ LIỆU ---
let plans = JSON.parse(localStorage.getItem('travelPlans')) || [];
let myChart = null; // Biến để chứa biểu đồ

// Lấy các thẻ HTML
const planForm = document.getElementById('plan-form');
const planList = document.getElementById('plan-list');
const emptyMsg = document.getElementById('empty-msg'); 
const filterStatus = document.getElementById('filter-status');
const searchInput = document.getElementById('search-keyword');
const btnClearAll = document.getElementById('btn-clear-all');

// Lấy các thẻ thống kê (MỚI)
const totalCountSpan = document.getElementById('total-count');
const percentDoneSpan = document.getElementById('percent-done');

// --- 2. HÀM VẼ GIAO DIỆN (Render) ---
function renderPlans() {
    if (!planList) return;
    planList.innerHTML = ''; 
    
    // Lấy giá trị lọc
    const statusValue = filterStatus ? filterStatus.value : 'all';
    const keyword = searchInput ? searchInput.value.toLowerCase() : '';

    // Lọc dữ liệu
    const filteredPlans = plans.filter(plan => {
        const matchStatus = (statusValue === 'all') || (plan.status === statusValue);
        const matchSearch = (plan.title || '').toLowerCase().includes(keyword);
        return matchStatus && matchSearch;
    });

    // Hiện thông báo nếu danh sách trống
    if (filteredPlans.length === 0) {
        if (emptyMsg) emptyMsg.style.display = 'block';
    } else {
        if (emptyMsg) emptyMsg.style.display = 'none';
        
        filteredPlans.forEach((plan) => {
            const realIndex = plans.indexOf(plan);
            const item = document.createElement('div');
            item.className = `plan-item ${plan.priority}-priority ${plan.status === 'done' ? 'completed' : ''}`;
            
            item.innerHTML = `
                <div class="plan-info">
                    <h3>
                        ${plan.title} 
                        <span class="badge ${plan.priority}">${getPriorityLabel(plan.priority)}</span>
                    </h3>
                    <p class="time"><i class="far fa-clock"></i> ${formatDate(plan.deadline)}</p>
                    <p class="desc">${plan.description}</p>
                </div>
                <div class="plan-actions">
                    <button type="button" onclick="toggleStatus(${realIndex})" class="btn-check"><i class="fas fa-check"></i></button>
                    <button type="button" onclick="deletePlan(${realIndex})" class="btn-delete"><i class="fas fa-trash"></i></button>
                </div>
            `;
            planList.appendChild(item);
        });
    }

    // 🔥 CẬP NHẬT 3: Gọi hàm vẽ biểu đồ mỗi khi render lại
    updateStatsAndChart();
}

// --- 3. HÀM VẼ BIỂU ĐỒ & THỐNG KÊ (MỚI) ---
function updateStatsAndChart() {
    const total = plans.length;
    const done = plans.filter(p => p.status === 'done').length;
    const pending = total - done;

    // Cập nhật số liệu text
    if (totalCountSpan) totalCountSpan.innerText = total;
    if (percentDoneSpan) percentDoneSpan.innerText = total === 0 ? '0%' : Math.round((done / total) * 100) + '%';

    // Vẽ biểu đồ tròn (Doughnut Chart)
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
    type: 'doughnut', // Hoặc 'pie'
    data: {
        labels: ['Đã đi', 'Chưa đi'],
        datasets: [{
            data: [2, 5], // Dữ liệu mẫu
            backgroundColor: ['#2ecc71', '#ff4757'],
        }]
    },
    options: {
        plugins: {
            legend: {
                display: true,
                position: 'right', // Cho chú thích sang bên phải
                align: 'center',   // Căn giữa theo chiều dọc của chart
                labels: {
                    boxWidth: 20,  // Độ rộng của ô màu xanh/đỏ
                    padding: 15,   // Khoảng cách giữa các dòng chú thích
                    font: { size: 14 }
                }
            }
        },
        maintainAspectRatio: false
    }
});
}

// --- 4. CÁC HÀM PHỤ TRỢ ---
function getPriorityLabel(priority) {
    if (priority === 'high') return 'Must Go';
    if (priority === 'medium') return 'Should Go';
    return 'Chill';
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString('vi-VN', {hour:'2-digit', minute:'2-digit', day:'2-digit', month:'2-digit', year:'numeric'});
}

function saveToLocal() {
    localStorage.setItem('travelPlans', JSON.stringify(plans));
}

// --- 5. XỬ LÝ SỰ KIỆN ---

if (planForm) {
    planForm.addEventListener('submit', function(e) {
        e.preventDefault(); 
        const title = document.getElementById('title').value;
        const deadline = document.getElementById('deadline').value;
        const priority = document.getElementById('priority').value;
        const description = document.getElementById('description').value;

        if (new Date(deadline) < new Date()) {
            alert('❌ Ngày đi không được ở quá khứ!');
            return;
        }

        plans.push({ title, deadline, priority, description, status: 'pending' });
        
        if (filterStatus) filterStatus.value = 'all';
        if (searchInput) searchInput.value = '';

        saveToLocal();
        renderPlans();
        planForm.reset();
    });
}

window.deletePlan = function(index) {
    if (confirm('Xóa địa điểm này nhé?')) {
        plans.splice(index, 1);
        saveToLocal();
        renderPlans();
    }
};

window.toggleStatus = function(index) {
    plans[index].status = plans[index].status === 'pending' ? 'done' : 'pending';
    saveToLocal();
    renderPlans();
};

if (searchInput) searchInput.addEventListener('input', renderPlans);
if (filterStatus) filterStatus.addEventListener('change', renderPlans);

if (btnClearAll) {
    btnClearAll.addEventListener('click', function() {
        if (confirm('Bạn chắc chắn muốn xóa TOÀN BỘ lịch trình không?')) {
            plans = [];
            saveToLocal();
            renderPlans();
        }
    });
}

// Chạy lần đầu
renderPlans();
