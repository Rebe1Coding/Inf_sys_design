// API клиент для взаимодействия с backend

const API = {
    baseUrl: '/api',

    /**
     * Получить список клиентов
     */
     getClients(page = 1, pageSize = 10, ownershipFilter = '', sortField = '') {
        const params = new URLSearchParams({
            page: page,
            page_size: pageSize
        });

        if (ownershipFilter) {
            params.append('ownership_filter', ownershipFilter);
        }

        if (sortField) {
            params.append('sort_field', sortField);
        }

        const response =  fetch(`${this.baseUrl}/clients?${params}`);
        
        if (!response.ok) {
            throw new Error('Ошибка при загрузке клиентов');
        }

        return  response.json();
    },

    /**
     * Получить детальную информацию о клиенте
     */
    async getClientDetail(clientId) {
        const response =  fetch(`${this.baseUrl}/clients/${clientId}`);
        
        if (!response.ok) {
            throw new Error('Клиент не найден');
        }

        return  response.json();
    },

    /**
     * Добавить нового клиента
     */
     addClient(clientData) {
        const response =  fetch(`${this.baseUrl}/clients`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(clientData)
        });

        const result =  response.json();
        
        if (!response.ok) {
            throw result;
        }

        return result;
    },

    /**
     * Обновить данные клиента
     */
     updateClient(clientId, clientData) {
        const response =  fetch(`${this.baseUrl}/clients/${clientId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(clientData)
        });

        const result =  response.json();
        
        if (!response.ok) {
            throw result;
        }

        return result;
    },

    /**
     * Удалить клиента
     */
     deleteClient(clientId) {
        const response =  fetch(`${this.baseUrl}/clients/${clientId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Ошибка при удалении клиента');
        }

        return  response.json();
    },

    /**
     * Получить данные для формы (универсальный endpoint)
     */
     getFormData(mode, clientId = null) {
        const params = clientId ? `?client_id=${clientId}` : '';
        const response =  fetch(`${this.baseUrl}/form/${mode}${params}`);
        
        if (!response.ok) {
            throw new Error('Ошибка при загрузке формы');
        }

        return  response.json();
    },

    /**
     * Отправить форму (универсальный endpoint)
     */
     submitForm(mode, clientData, clientId = null) {
        const params = new URLSearchParams({ mode });
        if (clientId) {
            params.append('client_id', clientId);
        }

        const response =  fetch(`${this.baseUrl}/form/submit?${params}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(clientData)
        });

        const result = response.json();
        
        if (!response.ok) {
            throw result;
        }

        return result;
    }
};