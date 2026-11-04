pipeline {
    agent any

    stages {
        stage('Start QEMU with OpenBMC') {
            steps {
                echo 'Запускаем QEMU с образом OpenBMC в фоне...'
                sh '''
                    pkill -f qemu-system-arm || true
                    
                    nohup qemu-system-arm -m 256 -M romulus-bmc -nographic \
                    -drive file=/workspace/romulus/romulus.mtd,format=raw,if=mtd \
                    -net nic -net user,hostfwd=:0.0.0.0:2222-:22,hostfwd=:0.0.0.0:2443-:443,hostfwd=udp:0.0.0.0:2623-:623,hostname=qemu > /tmp/qemu.log 2>&1 &
                '''
            }
        }

        stage('Wait for OpenBMC to boot') {
            steps {
                echo 'Ожидаем загрузку OpenBMC (проверяем доступность Redfish API)...'
                sh '''
                    for i in $(seq 1 60); do
                        if curl -k -s -u root:0penBmc https://localhost:2443/redfish/v1/ | grep -q "RedfishVersion"; then
                            echo "OpenBMC готов к работе!"
                            exit 0
                        fi
                        echo "Попытка $i: BMC еще грузится, ждем 5 секунд..."
                        sleep 5
                    done
                    echo "ОШИБКА: OpenBMC не загрузился за 5 минут!"
                    cat /tmp/qemu.log
                    exit 1
                '''
            }
        }

        stage('Run API Tests (Redfish)') {
            steps {
                echo 'Запускаем API-тесты (PyTest + Requests)...'
                sh '''
                    cd /workspace/ci-cd-lab/api_tests
                    mkdir -p reports
                    pytest test_redfish.py --html=reports/api_report.html --self-contained-html || true
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                echo 'Запускаем UI-тесты (Selenium)...'
                sh '''
                    cd /workspace/ci-cd-lab/selenium_tests
                    mkdir -p reports
                    export CHROME_BIN=/usr/bin/chromium
                    pytest --html=reports/selenium_report.html --self-contained-html || true
                '''
            }
        }

        stage('Run Load Tests') {
            steps {
                echo 'Запускаем нагрузочные тесты (Locust)...'
                sh '''
                    cd /workspace/ci-cd-lab/locust_tests
                    mkdir -p reports
                    locust -f locustfile_openbmc.py --headless -u 2 -r 1 -t 30s --html reports/locust_openbmc.html || true
                    locust -f locustfile_public.py --headless -u 2 -r 1 -t 30s --html reports/locust_public.html || true
                '''
            }
        }
    }

    post {
        always {
            echo 'Сохраняем артефакты (HTML-отчеты)...'
            archiveArtifacts artifacts: '**/reports/*.html', allowEmptyArchive: true
            
            echo 'Останавливаем QEMU...'
            sh 'pkill -f qemu-system-arm || true'
            
            echo 'Выводим лог QEMU (для диагностики, если что-то упало)...'
            sh 'cat /tmp/qemu.log || true'
        }
    }
}