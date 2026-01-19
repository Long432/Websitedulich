// --- 1. KHỞI TẠO DỮ LIỆU ---
// Lấy dữ liệu từ bộ nhớ, nếu không có thì tạo mảng rỗng
let plans = JSON.parse(localStorage.getItem('travelPlans')) || [];

// Lấy các thẻ HTML cần dùng (Đảm bảo HTML của cậu đã có các ID này)
const planForm = document.getElementById('plan-form');
const planList = document.getElementById('plan-list');
const emptyMsg = document.getElementById('empty-msg'); 
const filterStatus = document.getElementById('filter-status');
const searchInput = document.getElementById('search-keyword');
const btnClearAll = document.getElementById('btn-clear-all');

// --- 2. HÀM VẼ GIAO DIỆN (Render) ---
function renderPlans() {
    // Nếu HTML thiếu thẻ plan-list thì dừng lại để tránh lỗi
    if (!planList) return;

    planList.innerHTML = ''; // Xóa danh sách cũ
    
    // Lấy giá trị lọc (Xử lý lỗi nếu không có ô lọc)
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
        
        // Vẽ từng thẻ
        filteredPlans.forEach((plan) => {
            // Tìm vị trí thực của plan trong mảng gốc để xử lý Xóa/Sửa đúng cái
            const realIndex = plans.indexOf(plan);

            const item = document.createElement('div');
            // Thêm class màu sắc
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
}

// --- 3. CÁC HÀM PHỤ TRỢ ---
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

// --- 4. XỬ LÝ SỰ KIỆN ---

// SỰ KIỆN 1: Thêm mới
if (planForm) {
    planForm.addEventListener('submit', function(e) {
        e.preventDefault(); // <--- DÒNG QUAN TRỌNG NHẤT: CHẶN LOAD LẠI TRANG

        // Lấy dữ liệu
        const title = document.getElementById('title').value;
        const deadline = document.getElementById('deadline').value;
        const priority = document.getElementById('priority').value;
        const description = document.getElementById('description').value;

        // Kiểm tra ngày tháng
        if (new Date(deadline) < new Date()) {
            alert('❌ Ngày đi không được ở quá khứ!');
            return;
        }

        // Thêm vào mảng
        plans.push({ 
            title: title, 
            deadline: deadline, 
            priority: priority, 
            description: description, 
            status: 'pending' 
        });

        // Tự động Reset bộ lọc về "Tất cả" để nhìn thấy cái mới thêm
        if (filterStatus) filterStatus.value = 'all';
        if (searchInput) searchInput.value = '';

        saveToLocal();
        renderPlans();
        planForm.reset(); // Xóa trắng form
    });
}

// SỰ KIỆN 2: Các nút chức năng (Global)
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

// SỰ KIỆN 3: Tìm kiếm & Lọc
if (searchInput) searchInput.addEventListener('input', renderPlans);
if (filterStatus) filterStatus.addEventListener('change', renderPlans);

// SỰ KIỆN 4: Xóa hết
if (btnClearAll) {
    btnClearAll.addEventListener('click', function() {
        if (confirm('Bạn chắc chắn muốn xóa TOÀN BỘ lịch trình không?')) {
            plans = [];
            saveToLocal();
            renderPlans();
        }
    });
}

// --- 5. CHẠY LẦN ĐẦU ---
console.log("File JS đã chạy thành công!"); // Kiểm tra Console xem có dòng này không
renderPlans();
