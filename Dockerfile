# ОФИЦИАЛЬНЫЙ образ Playwright для Python (Ubuntu 22.04 LTS)
# Он уже содержит Python, браузеры и ВСЕ системные зависимости!
FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

# Рабочая директория в контейнере
WORKDIR /app

# Копируем зависимости и устанавливаем их
# (Playwright уже есть в образе, pip просто проверит версии остальных библиотек)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Команда по умолчанию: запускаем тесты параллельно
CMD ["pytest", "tests/", "-v", "-n", "auto", "--alluredir=allure-results"]