#常规3.5账号批发格式的txt再次进行格式化, 方便读?
def extract_account_password(line):
    """
    Extracts account and password from a line based on the specified rules.
    """
    account_start = line.find('账号') + 2  # 账号的开始位置
    password_start = line.find('密码') + 2  # 密码的开始位置

    # 提取账号
    account_end = password_start - 2  # 账号的结束位置
    account = line[account_start:account_end]

    # 提取密码
    # 找到密码后的第一个中文字符的位置作为密码的结束位置
    for i in range(password_start, len(line)):
        if '\u4e00' <= line[i] <= '\u9fff':  # 检查字符是否为中文
            password = line[password_start:i]
            break
    else:
        password = line[password_start:]  # 如果没有中文字符，则取到行尾

    return account, password

def process_accounts(file_path):
    accounts = []
    passwords = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            account, password = extract_account_password(line)
            accounts.append(account)
            passwords.append(password)

    return accounts, passwords

def save_formatted_accounts(accounts, passwords, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for account, password in zip(accounts, passwords):
            file.write(f"{account}--{password}\n")

# 主程序
input_file = 'accounts.txt'
output_file = 'formated_accounts.txt'

accounts, passwords = process_accounts(input_file)
save_formatted_accounts(accounts, passwords, output_file)
