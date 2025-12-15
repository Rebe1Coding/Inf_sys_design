from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Добавляем корневую директорию в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories.client_rep_db import Client_rep_DB
from repositories.repository import ClientDBAdapter
from config.db_conn import db_conn
from web.observer.repository_observer import RepositoryObserver
from web.controllers.main_controller import MainController
from web.controllers.add_controller import AddController
from web.controllers.edit_controller import EditController
from web.controllers.form_controller import FormController

# Инициализация FastAPI
app = FastAPI(title="Client Management System")

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Инициализация репозитория с паттерном Наблюдатель
db_repo = Client_rep_DB(db_conn)
adapter = ClientDBAdapter(db_repo)
repository = RepositoryObserver(adapter)

# Pydantic модели для валидации запросов
class ClientCreate(BaseModel):
    name: str
    ownership_type: str
    address: str
    phone: str
    contact_person: str

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    ownership_type: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    contact_person: Optional[str] = None


# ============= ГЛАВНАЯ СТРАНИЦА (VIEW) =============
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Главная страница приложения"""
    return templates.TemplateResponse("index.html", {"request": request})


# ============= API ENDPOINTS (CONTROLLER) =============

@app.get("/api/clients")
def get_clients(
    page: int = 1, 
    page_size: int = 10,
    ownership_filter: Optional[str] = None,
    sort_field: Optional[str] = None
):
    """Получить список клиентов с пагинацией, фильтрацией и сортировкой"""
    controller = MainController(repository)
    result = controller.get_clients_page(page, page_size, ownership_filter, sort_field)
    return JSONResponse(content=result)


@app.get("/api/clients/{client_id}")
def get_client_detail(client_id: int):
    """Получить полную информацию о клиенте"""
    controller = MainController(repository)
    client = controller.get_client_detail(client_id)
    
    if client:
        return JSONResponse(content=client)
    else:
        raise HTTPException(status_code=404, detail="Клиент не найден")


@app.post("/api/clients")
def add_client(client_data: ClientCreate):
    """Добавить нового клиента"""
    controller = AddController(repository)
    result = controller.validate_and_add(client_data.dict())
    
    if result["success"]:
        return JSONResponse(content=result, status_code=201)
    else:
        return JSONResponse(content=result, status_code=400)


@app.put("/api/clients/{client_id}")
def update_client(client_id: int, client_data: ClientUpdate):
    """Обновить данные клиента"""
    controller = EditController(repository)
    # Фильтруем только непустые поля
    update_data = {k: v for k, v in client_data.dict().items() if v is not None}
    result = controller.validate_and_update(client_id, update_data)
    
    if result["success"]:
        return JSONResponse(content=result)
    else:
        return JSONResponse(content=result, status_code=400)


@app.delete("/api/clients/{client_id}")
def delete_client(client_id: int):
    """Удалить клиента"""
    success = repository.delete_client(client_id)
    
    if success:
        return JSONResponse(content={
            "success": True,
            "message": "Клиент успешно удален"
        })
    else:
        raise HTTPException(status_code=404, detail="Клиент не найден")


# ============= API ДЛЯ ФОРМЫ (рефакторинг п.4) =============

@app.get("/api/form/{mode}")
def get_form_data(mode: str, client_id: Optional[int] = None):
    """Получить данные для формы (add или edit)"""
    controller = FormController(repository, mode, client_id)
    form_data = controller.get_form_data()
    return JSONResponse(content=form_data)


@app.post("/api/form/submit")
def submit_form(
    mode: str,
    client_id: Optional[int] = None,
    client_data: ClientCreate = None
):
    """Отправить форму (универсальный endpoint для add и edit)"""
    controller = FormController(repository, mode, client_id)
    result = controller.submit_form(client_data.dict())
    
    if result["success"]:
        return JSONResponse(content=result)
    else:
        return JSONResponse(content=result, status_code=400)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)