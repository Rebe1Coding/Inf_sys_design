// Глобальные переменные
let currentPage = 1;
let pageSize = 10;
let currentFilter = '';
let currentSort = 'client_id';

/**
 * Инициализация приложения
 */
document.addEventListener('DOMContentLoaded', () => {
    // Загрузка начальных данных
    loadClients();

    // Обработчики событий
    document.getElementById('addClientBtn').addEventListener('click', () => openFormModal('add'));
    document.getElementById('ownershipFilter').addEventListener('change', (e) => {
        currentFilter = e.target.value;
        currentPage = 1;
        loadClients();
    });
    document.getElementById('sortField').addEventListener('change', (e) => {
        currentSort = e.target.value;
        currentPage = 1;
        loadClients();
    });

    // Обработка отправки формы
    document.getElementById('clientForm').addEventListener('submit', handleFormSubmit);
});

/**
 * Загрузка списка клиентов
 */
window.loadClients = async function() {
    const tbody = document.getElementById('clientsTableBody');
    tbody.innerHTML = '<tr><td colspan="5" class="loading">Загрузка</td></tr>';

    try {
        const data = await API.getClients(currentPage, pageSize, currentFilter, currentSort);
        
        // Отображаем клиентов
        renderClientsTable(data.clients);
        
        // Отображаем пагинацию
        renderPagination(data.current_page, data.total_pages);
        
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:red;">Ошибка загрузки данных</td></tr>';
    }
}

/**
 * Отображение таблицы клиентов
 */
function renderClientsTable(clients) {
    const tbody = document.getElementById('clientsTableBody');
    
    if (clients.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;">Нет данных</td></tr>';
        return;
    }

    tbody.innerHTML = clients.map((client, index) => {
        // Парсим строку формата "Название (Контактное лицо)"
        const parts = client.match(/^(.+?)\s*\((.+?)\)$/);
        const name = parts ? parts[1] : client;
        const contact = parts ? parts[2] : '';
        
        return `
            <tr onclick="showClientDetail(${currentPage * pageSize - pageSize + index + 1})">
                <td>${currentPage * pageSize - pageSize + index + 1}</td>
                <td>${name}</td>
                <td>-</td>
                <td>-</td>
                <td class="actions" onclick="event.stopPropagation()">
                    <button class="btn btn-info" onclick="showClientDetail(${currentPage * pageSize - pageSize + index + 1})">Детали</button>
                    <button class="btn btn-success" onclick="openFormModal('edit', ${currentPage * pageSize - pageSize + index + 1})">Изменить</button>
                    <button class="btn btn-danger" onclick="deleteClient(${currentPage * pageSize - pageSize + index + 1})">Удалить</button>
                </td>
            </tr>
        `;
    }).join('');
}

/**
 * Отображение пагинации
 */
function renderPagination(current, total) {
    const pagination = document.getElementById('pagination');
    
    if (total <= 1) {
        pagination.innerHTML = '';
        return;
    }

    let html = '';
    
    // Кнопка "Предыдущая"
    html += `<button ${current === 1 ? 'disabled' : ''} onclick="changePage(${current - 1})">‹ Предыдущая</button>`;
    
    // Номера страниц
    for (let i = 1; i <= total; i++) {
        if (i === 1 || i === total || (i >= current - 2 && i <= current + 2)) {
            html += `<button class="${i === current ? 'active' : ''}" onclick="changePage(${i})">${i}</button>`;
        } else if (i === current - 3 || i === current + 3) {
            html += '<button disabled>...</button>';
        }
    }
    
    // Кнопка "Следующая"
    html += `<button ${current === total ? 'disabled' : ''} onclick="changePage(${current + 1})">Следующая ›</button>`;
    
    pagination.innerHTML = html;
}

/**
 * Смена страницы
 */
function changePage(page) {
    currentPage = page;
    loadClients();
}

/**
 * Показать детальную информацию о клиенте
 */
async function showClientDetail(clientId) {
    const modal = document.getElementById('detailModal');
    const body = document.getElementById('detailModalBody');
    
    body.innerHTML = '<div class="loading">Загрузка</div>';
    modal.classList.add('show');

    try {
        const client = await API.getClientDetail(clientId);
        
        body.innerHTML = `
            <div class="detail-item">
                <strong>ID:</strong>
                ${client.client_id}
            </div>
            <div class="detail-item">
                <strong>Название:</strong>
                ${client.name}
            </div>
            <div class="detail-item">
                <strong>Тип собственности:</strong>
                ${client.ownership_type}
            </div>
            <div class="detail-item">
                <strong>Адрес:</strong>
                ${client.address}
            </div>
            <div class="detail-item">
                <strong>Телефон:</strong>
                ${client.phone}
            </div>
            <div class="detail-item">
                <strong>Контактное лицо:</strong>
                ${client.contact_person}
            </div>
        `;
    } catch (error) {
        body.innerHTML = '<div style="color:red;">Ошибка загрузки данных</div>';
    }
}

/**
 * Закрыть модальное окно детальной информации
 */
function closeDetailModal() {
    document.getElementById('detailModal').classList.remove('show');
}

/**
 * Открыть модальное окно формы
 */
async function openFormModal(mode, clientId = null) {
    const modal = document.getElementById('formModal');
    const title = document.getElementById('formModalTitle');
    const form = document.getElementById('clientForm');
    
    // Очистка формы
    form.reset();
    clearFormErrors();
    
    // Установка режима
    document.getElementById('formMode').value = mode;
    
    if (mode === 'add') {
        title.textContent = 'Добавление клиента';
        document.getElementById('clientId').value = '';
    } else {
        title.textContent = 'Редактирование клиента';
        
        try {
            const client = await API.getClientDetail(clientId);
            
            document.getElementById('clientId').value = client.client_id;
            document.getElementById('name').value = client.name;
            document.getElementById('ownershipType').value = client.ownership_type;
            document.getElementById('address').value = client.address;
            document.getElementById('phone').value = client.phone;
            document.getElementById('contactPerson').value = client.contact_person;
        } catch (error) {
            alert('Ошибка загрузки данных клиента');
            return;
        }
    }
    
    modal.classList.add('show');
}

/**
 * Закрыть модальное окно формы
 */
function closeFormModal() {
    document.getElementById('formModal').classList.remove('show');
}

/**
 * Обработка отправки формы
 */
async function handleFormSubmit(e) {
    e.preventDefault();
    
    clearFormErrors();
    
    const mode = document.getElementById('formMode').value;
    const clientId = document.getElementById('clientId').value;
    
    const formData = {
        name: document.getElementById('name').value.trim(),
        ownership_type: document.getElementById('ownershipType').value,
        address: document.getElementById('address').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        contact_person: document.getElementById('contactPerson').value.trim()
    };

    // Клиентская валидация
    const errors = validateForm(formData);
    if (errors.length > 0) {
        displayFormErrors(errors);
        return;
    }

    try {
        let result;
        
        if (mode === 'add') {
            result = await API.addClient(formData);
            clientObserver.notify('client_added', result.client);
        } else {
            result = await API.updateClient(clientId, formData);
            clientObserver.notify('client_updated', result.client);
        }
        
        closeFormModal();
        
    } catch (error) {
        console.error('Ошибка:', error);
        if (error.errors) {
            displayFormErrors(error.errors);
        } else {
            displayFormErrors([error.message || 'Произошла ошибка при сохранении']);
        }
    }
}

/**
 * Валидация формы на клиенте
 */
function validateForm(data) {
    const errors = [];
    
    if (!data.name || data.name.length < 2) {
        errors.push('Название должно содержать минимум 2 символа');
    }
    
    if (!data.ownership_type) {
        errors.push('Выберите тип собственности');
    }
    
    if (!data.address || data.address.length < 5) {
        errors.push('Адрес должен содержать минимум 5 символов');
    }
    
    if (!data.phone || data.phone.length < 7) {
        errors.push('Телефон должен содержать минимум 7 цифр');
    }
    
    if (!data.contact_person || data.contact_person.length < 2) {
        errors.push('ФИО должно содержать минимум 2 символа');
    }
    
    return errors;
}

/**
 * Отображение ошибок валидации
 */
function displayFormErrors(errors) {
    const errorSummary = document.getElementById('formErrors');
    errorSummary.innerHTML = errors.map(err => `<div>• ${err}</div>`).join('');
    errorSummary.classList.add('show');
}

/**
 * Очистка ошибок валидации
 */
function clearFormErrors() {
    const errorSummary = document.getElementById('formErrors');
    errorSummary.classList.remove('show');
    errorSummary.innerHTML = '';
    
    // Очистка индивидуальных ошибок
    document.querySelectorAll('.error').forEach(el => el.textContent = '');
}

/**
 * Удаление клиента
 */
async function deleteClient(clientId) {
    if (!confirm('Вы уверены, что хотите удалить этого клиента?')) {
        return;
    }

    try {
        await API.deleteClient(clientId);
        clientObserver.notify('client_deleted', clientId);
    } catch (error) {
        alert('Ошибка при удалении клиента');
        console.error(error);
    }
}

// Закрытие модальных окон при клике вне их
window.onclick = function(event) {
    const detailModal = document.getElementById('detailModal');
    const formModal = document.getElementById('formModal');
    
    if (event.target === detailModal) {
        closeDetailModal();
    }
    if (event.target === formModal) {
        closeFormModal();
    }
}