# Demand Forecasting MLOps Pipeline

Учебный MLOps-проект: автоматизированный пайплайн для прогнозирования спроса с использованием Docker, PostgreSQL, Airflow и Scikit-learn.

## 📌 О проекте
Проект симулирует работу реального продакшен-пайплайна в ритейле. Он демонстрирует полный цикл: от генерации данных до оркестрации задач по расписанию. 
Приложение читает исторические данные о продажах, обучает простую линейную регрессию, делает прогноз на 7 дней вперед и сохраняет результаты в базу данных.

## 🏗 Архитектура

- **Application (`src/`):** Python-код для генерации данных, обучения модели и записи прогнозов.
- **Orchestrator (`infra/airflow/`):** Apache Airflow (Webserver + Scheduler) для запуска пайплайна по расписанию.
- **Database (`demand_db`):** PostgreSQL для хранения сырых данных, прогнозов и логов.
- **Containerization:** Docker и Docker Compose для изоляции окружения.
- **Dependency Management:** `uv` для быстрой и надежной установки зависимостей.
- **CI:** GitHub Actions для автоматического запуска тестов (`pytest`) при каждом коммите.

## 🔄 Как это работает (Sequence)

1. **Триггер:** Airflow Scheduler запускает DAG `daily_demand_forecast` (по расписанию `0 2 * * *` или вручную).
2. **Запуск контейнера:** Airflow через `DockerOperator` запускает контейнер `demand-pet-app:latest`.
3. **Работа приложения:** Внутри контейнера выполняется `src/pipeline.py`:
   - Подключение к базе данных PostgreSQL.
   - Чтение данных из таблицы `raw_sales`.
   - Обучение модели `LinearRegression`.
   - Генерация прогноза на 7 дней.
   - Запись прогноза в таблицу `predictions`.
   - Запись логов в `pipeline_logs`.
4. **Завершение:** Контейнер завершает работу (код 0) и автоматически удаляется (`auto_remove=True`).

## 🚀 Как запустить проект

### Предварительные требования
- Docker Desktop (запущен)
- Git

### 1. Клонирование репозитория
```bash
git clone https://github.com/Mabaz/demand-pet.git
cd demand-pet
```

### 2. Настройка окружения
Создайте файл `.env` в корне проекта (на основе `.env.example`):
```dotenv
POSTGRES_USER=pet_user
POSTGRES_PASSWORD=pet_password
POSTGRES_DB=pet_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 3. Запуск базы данных
```bash
docker compose up -d db
```

### 4. Сборка образа приложения
```bash
docker compose build
```

### 5. Наполнение базы тестовыми данными
```bash
docker compose run --rm app uv run python -m src.seed
```

### 6. Запуск Airflow (Оркестратор)
```bash
cd infra
docker compose -f docker-compose.airflow.yml up -d
```
*Первый запуск может занять пару минут. Если контейнер `airflow-webserver` упал, просто перезапустите его: `docker compose -f docker-compose.airflow.yml restart airflow-webserver`.*

### 7. Запуск пайплайна
1. Откройте Airflow UI: `http://localhost:8080` (логин: `admin`, пароль: `admin`).
2. Включите (Unpause) DAG `daily_demand_forecast`.
3. Нажмите **Trigger DAG** (Play ▶️).
4. Дождитесь зеленого статуса задачи.

### 8. Проверка результатов
Подключитесь к базе данных `pet_db` (например, через DBeaver) и проверьте таблицы:
- `raw_sales` — исходные данные.
- `predictions` — новые прогнозы.
- `pipeline_logs` — логи работы пайплайна.

## 🧪 Тестирование
```bash
uv run pytest
```

## 📂 Структура проекта
```text
demand-pet/
├── src/                    # Код приложения
├── tests/                  # Тесты
├── infra/                  # Инфраструктура (Airflow)
│   ├── airflow/
│   │   ├── Dockerfile
│   │   └── dags/
│   └── docker-compose.airflow.yml
├── .github/workflows/      # CI/CD
├── Dockerfile              # Инструкция для сборки приложения
├── docker-compose.yml      # Локальный запуск (App + DB)
└── pyproject.toml          # Зависимости
```

## 🛠 Стек технологий
- **Python 3.11**, **Pandas**, **Scikit-learn**
- **PostgreSQL 16**
- **Apache Airflow 2.9**
- **Docker**, **Docker Compose**
- **uv**
- **pytest**