/**
 * Реализация паттерна Наблюдатель на стороне клиента
 */

class ClientObserver {
    constructor() {
        this.observers = [];
    }

    /**
     * Подписать наблюдателя
     */
    subscribe(observer) {
        if (typeof observer !== 'function') {
            throw new Error('Observer должен быть функцией');
        }
        this.observers.push(observer);
    }

    /**
     * Отписать наблюдателя
     */
    unsubscribe(observer) {
        this.observers = this.observers.filter(obs => obs !== observer);
    }

    /**
     * Уведомить всех наблюдателей
     */
    notify(eventType, data) {
        this.observers.forEach(observer => {
            observer(eventType, data);
        });
    }
}

// Глобальный экземпляр наблюдателя
const clientObserver = new ClientObserver();

/**
 * Обработчики событий для разных типов операций
 */
const ClientEventHandlers = {
    /**
     * Обработка добавления клиента
     */
    onClientAdded: (data) => {
        console.log('Клиент добавлен:', data);
        // Автоматически обновляем таблицу
        if (window.loadClients) {
            window.loadClients();
        }
    },

    /**
     * Обработка обновления клиента
     */
    onClientUpdated: (data) => {
        console.log('Клиент обновлен:', data);
        // Автоматически обновляем таблицу
        if (window.loadClients) {
            window.loadClients();
        }
    },

    /**
     * Обработка удаления клиента
     */
    onClientDeleted: (data) => {
        console.log('Клиент удален:', data);
        // Автоматически обновляем таблицу
        if (window.loadClients) {
            window.loadClients();
        }
    }
};

// Подписываем обработчики на события
clientObserver.subscribe((eventType, data) => {
    switch (eventType) {
        case 'client_added':
            ClientEventHandlers.onClientAdded(data);
            break;
        case 'client_updated':
            ClientEventHandlers.onClientUpdated(data);
            break;
        case 'client_deleted':
            ClientEventHandlers.onClientDeleted(data);
            break;
        default:
            console.log('Неизвестный тип события:', eventType);
    }
});