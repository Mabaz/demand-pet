from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

with DAG(
    dag_id="daily_demand_forecast",
    start_date=datetime(2024, 1, 1),
    schedule="0 2 * * *",  # Запуск каждый день в 02:00 ночи
    catchup=False,
    tags=["ml", "forecast"],
) as dag:

    run_pipeline = DockerOperator(
        task_id="run_forecast_pipeline",
        # Имя образа, который мы собрали в основном проекте
        image="demand-pet-app:latest", 
        command="uv run --no-sync python -m src.pipeline",
        # ⚠️ Важно: передаем переменные окружения внутрь контейнера
        environment={
            "POSTGRES_USER": "pet_user",
            "POSTGRES_PASSWORD": "pet_password",
            "POSTGRES_DB": "pet_db",
            "POSTGRES_HOST": "demand_db", # Имя контейнера с нашей БД!
            "POSTGRES_PORT": "5432",
        },
        # Подключаем контейнер к той же сети, где живет наша БД
        network_mode="demand-pet_default", 
        docker_url="unix://var/run/docker.sock",
        auto_remove=True, # Удалить контейнер после выполнения (ephemeral)
    )