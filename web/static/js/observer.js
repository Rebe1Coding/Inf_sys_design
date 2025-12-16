/**
 * Реализация паттерна Наблюдатель на стороне клиента
 */

class ClientObserver {
    constructor() {
        this.observers = [];
    }
    subscribe(observer) {
        if (typeof observer !== 'function') {
            throw new Error('Observer должен быть функцией');
        }
        this.observers.push(observer);
    }


    unsubscribe(observer) {
        this.observers = this.observers.filter(obs => obs !== observer);
    }


    notify(eventType, data) {
        this.observers.forEach(observer => {
            observer(eventType, data);
        });
    }
}


const clientObserver = new ClientObserver();

const ClientEventHandlers = {

    onClientAdded: (data) => {
        console.log('Клиент добавлен:', data);
        // Автоматически обновляем таблицу
        if (window.loadClients) {
            window.loadClients();
        }
    },

    onClientUpdated: (data) => {
        console.log('Клиент обновлен:', data);
        // Автоматически обновляем таблицу
        if (window.loadClients) {
            window.loadClients();
        }
    },

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