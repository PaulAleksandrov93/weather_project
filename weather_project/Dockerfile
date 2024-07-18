# Используем официальный образ Python
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы requirements.txt в контейнер
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Проверка установленных пакетов
RUN pip list

# Копируем оставшиеся файлы проекта в контейнер
COPY . /app

# Команда для запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]