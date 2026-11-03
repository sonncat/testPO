pipeline {
    agent any

    stages {
        stage('Start QEMU with OpenBMC') {
            steps {
                echo 'Запускаем QEMU с образом OpenBMC в фоне...'
                // Запускаем QEMU в фоне, чтобы Jenkins не завис
                sh '''
                    nohup qemu-system-arm -m 256 -M romulus-bmc -nographic \
                    -drive file=/workspace/romulus/romulus.mtd,format=raw,if=mtd \
                    -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu > /tmp/qemu.log 2>&1 &
                '''
            }
        }

        stage('Wait for OpenBMC to boot') {
            steps {
                echo 'Ожидаем загрузку OpenBMC (проверяем доступность Redfish API)...'
                // Ждем, пока BMC начнет отвечать на запросы (максимум 3 минуты)
                sh '''
                    for i in $(seq 1 36); do
                        if curl -k -s -u root:0penBmc https://localhost:2443/redfish/v1/ | grep -q "RedfishVersion"; then
                            echo "OpenBMC готов к работе!"
                            exit 0
                        fi
                        echo "Попытка $i: BMC еще грузится, ждем 5 секунд..."
                        sleep 5
                    done
                    echo "Ошибка: OpenBMC не загрузился за 3 минуты!"
                    cat /tmp/qemu.log
                    exit 1
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo 'Запускаем UI-тесты (Selenium)...'
                // Переходим в папку с тестами, создаем папку reports и запускаем pytest.
                // Флаг || true нужен, чтобы пайплайн не упал полностью, если тест не прошел (для отчета)
                sh '''
                    cd /workspace/ci-cd-lab/selenium_tests
                    mkdir -p reports
                    pytest --html=reports/selenium_report.html --self-contained-html || true
                '''
            }
        }

        stage('Run Load Tests') {
            steps {
                echo 'Запускаем нагрузочные тесты (Locust)...'
                // Запускаем Locust в headless-режиме (без браузера) и сохраняем HTML-отчет
                sh '''
                    cd /workspace/ci-cd-lab/locust_tests
                    mkdir -p reports
                    locust -f locustfile_openbmc.py --headless -u 5 -r 1 -t 20s --html reports/locust_openbmc.html || true
                    locust -f locustfile_public.py --headless -u 5 -r 1 -t 20s --html reports/locust_public.html || true
                '''
            }
        }
    }

    post {
        always {
            echo 'Сохраняем артефакты (отчеты тестов)...'
            // Собираем все сгенерированные HTML-отчеты
            archiveArtifacts artifacts: '**/reports/*.html', allowEmptyArchive: true
            
            echo 'Останавливаем QEMU...'
            // Убиваем процесс QEMU, чтобы он не занимал порты после завершения сборки
            sh 'pkill -f qemu-system-arm || true'
        }
    }
}
