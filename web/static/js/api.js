// API клиент для взаимодействия с backend

const API = {
    baseUrl: '/api',

    async getClients(page = 1, pageSize = 10, ownershipFilter = '', sortField = '') {
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

        const response = await fetch(`${this.baseUrl}/clients?${params}`);
        
        if (!response.ok) {
            throw new Error('Ошибка при загрузке клиентов');
        }

        return await response.json();
    },

    async getClientDetail(clientId) {
        const response = await fetch(`${this.baseUrl}/clients/${clientId}`);
        
        if (!response.ok) {
            throw new Error('Клиент не найден');
        }

        return await response.json();
    },

    async addClient(clientData) {
        const response = await fetch(`${this.baseUrl}/clients`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(clientData)
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw result;
        }

        return result;
    },

    async updateClient(clientId, clientData) {
        const response = await fetch(`${this.baseUrl}/clients/${clientId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(clientData)
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw result;
        }

        return result;
    },

    async deleteClient(clientId) {
        const response = await fetch(`${this.baseUrl}/clients/${clientId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Ошибка при удалении клиента');
        }

        return await response.json();
    },


    async getFormData(mode, clientId = null) {
        const params = clientId ? `?client_id=${clientId}` : '';
        const response = await fetch(`${this.baseUrl}/form/${mode}${params}`);
        
        if (!response.ok) {
            throw new Error('Ошибка при загрузке формы');
        }

        return await response.json();
    },

    async submitForm(mode, clientData, clientId = null) {
        const params = new URLSearchParams({ mode });
        if (clientId) {
            params.append('client_id', clientId);
        }

        const response = await fetch(`${this.baseUrl}/form/submit?${params}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(clientData)
        });

        const result = await response.json();
        
        if (!response.ok) {
            throw result;
        }

        return result;
    }
};