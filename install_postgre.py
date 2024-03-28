import sys
import subprocess

def update_hosts_file(ip_address):
    """
    Обновляет файл hosts, заменяя IP-адрес хоста на указанный адрес и обновляя имя пользователя для подключения по SSH.

    :param ip_address: Новый IP-адрес хоста.
    """
    try:
        # Читаем содержимое файла hosts
        with open('hosts', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("Hosts file not found")
        return

    updated_lines = []
    # Обновляем каждую строку в файле hosts
    for line in lines:
        if 'ansible_host' in line:
            # Запрашиваем имя пользователя у пользователя
            username = input("Enter the username for Ansible: ")
            # Если строка содержит ansible_host, заменяем IP-адрес и имя пользователя
            updated_line = f'{line.split()[0]} ansible_host={ip_address} ansible_user={username}\n'
            updated_lines.append(updated_line)
        else:
            # В остальных случаях оставляем строку без изменений
            updated_lines.append(line)

    try:
        # Перезаписываем файл hosts с обновленными данными
        with open('hosts', 'w') as f:
            f.writelines(updated_lines)
        print("Updated hosts file")
    except PermissionError:
        print("Permission denied to update hosts file")

    # Заменяем адрес в файле test.sh
    replace_address_in_test_sh(ip_address)

def replace_address_in_test_sh(ip_address):
    """
    Обновляет IP-адрес в файле test.sh.

    :param ip_address: Новый IP-адрес для подключения к PostgreSQL.
    """
    try:
        # Читаем содержимое файла test.sh
        with open('test.sh', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("test.sh file not found")
        return

    updated_lines = []
    # Обновляем каждую строку в файле test.sh
    for line in lines:
        if 'psql -h' in line:
            # Если строка содержит вызов psql, заменяем IP-адрес
            updated_line = f'psql -h {ip_address} -U postgres -c "SELECT 1;"\n'
            updated_lines.append(updated_line)
        else:
            # В остальных случаях оставляем строку без изменений
            updated_lines.append(line)

    try:
        # Перезаписываем файл test.sh с обновленными данными
        with open('test.sh', 'w') as f:
            f.writelines(updated_lines)
        print("Updated test file")
    except PermissionError:
        print("Permission denied to update test.sh file")

def run_commands():
    """
    Запускает необходимые команды Ansible для установки PostgreSQL и запускает файл test.sh.
    """
    commands = [
        "ansible-galaxy install --force -r requirements.yml  > /dev/null 2>&1",
        "ansible-playbook playbook.yml > /dev/null 2>&1"
    ]
    for command in commands:
        # Запускаем каждую команду в оболочке и игнорируем вывод
        result = subprocess.run(command, shell=True)
        if result.returncode != 0:
            print(f"Failed to execute command: {command}")
            sys.exit(1)

    # Проверяем успешное выполнение всех команд Ansible
    print("All Ansible commands executed successfully")

    # После выполнения всех команд запускаем test.sh и игнорируем вывод
    subprocess.run("./test.sh > /dev/null 2>&1", shell=True)
    print("PostgreSQL server installed and ready for remote job")

if __name__ == "__main__":
    # Проверяем, что передан корректный количество аргументов командной строки
    if len(sys.argv) != 2:
        print("Usage: python install_postgre.py <IP_address>")
        sys.exit(1)
    
    # Получаем IP-адрес из аргумента командной строки
    ip_address = sys.argv[1]

    # Обновляем файл hosts и заменяем адрес в файле test.sh
    update_hosts_file(ip_address)

    # Запускаем необходимые команды Ansible и скрипт test.sh
    run_commands()
