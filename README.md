# Лабораторная работа 7: CI/CD для OpenBMC

Данный репозиторий содержит конфигурацию пайплайна Jenkins для автоматизации тестирования OpenBMC.

## Стек
*   **Jenkins** (запущен в Docker)
*   **QEMU** (эмуляция OpenBMC)
*   **Pytest + Selenium** (UI-тесты)
*   **Locust** (нагрузочные тесты)

## Структура проекта
*   `Jenkinsfile` — основной скрипт пайплайна.
*   `Dockerfile` — кастомный образ Jenkins с установленным QEMU и Python-зависимостями.
*   `docker-compose.yml` — конфигурация для запуска Jenkins.
*   `selenium_tests/` — автотесты веб-интерфейса из ЛР №4.
*   `locust_tests/` — скрипты нагрузочного тестирования из ЛР №6.

## Этапы пайплайна
1.  **Start QEMU with OpenBMC** — запуск эмулятора BMC в фоне.
2.  **Wait for OpenBMC to boot** — ожидание загрузки (проверка доступности Redfish API).
3.  **Run Selenium Tests** — запуск UI-тестов.
4.  **Run Load Tests** — запуск нагрузочных тестов (Locust в headless-режиме).
5.  **Post-actions** — сбор HTML-отчетов в артефакты Jenkins и остановка QEMU.

## Как запустить локально
1. Установить Docker и Docker Compose.
2. Выполнить `docker compose up -d --build`.
3. Открыть Jenkins: `http://localhost:8080`.
4. Создать Pipeline Job, указав URL этого репозитория и путь к `Jenkinsfile`.
5. Нажать «Собрать сейчас».
