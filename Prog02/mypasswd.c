#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <shadow.h>
#include <unistd.h>
#include <pwd.h>
int main(){
	char user[100];
	printf("Enter Username: ");
	scanf("%s", user);
	struct spwd *spwd = getspnam(user); //truy xuất tên user trong /etc/shadow 
	char *password = getpass("Enter Old Password: "); //nhập lại mật khẩu cũ mà không bị lặp lại 
	char *ecrypted = crypt(password, spwd->sp_pwdp); // Mã hóa mật khẩu

	if(strcmp(ecrypted, spwd->sp_pwdp) != 0){ //So sánh 2 mật khẩu
		printf("Old Password is not correct !\n");
		return 0;
	}
	password = getpass("Enter New Password: "); //nhập mật khẩu mới 
	ecrypted = crypt(password, spwd->sp_pwdp); //Mã hóa mật khẩu mới
	spwd->sp_pwdp = ecrypted; //cập nhật mật khẩu mới vào con trỏ spwd

	FILE *file = fopen("/etc/shadow", "r"); // mở tệp /etc/shadow với chế độ read
	FILE *fileTemp = fopen("/tmp/replace.tmp", "w"); // mở tệp /tmp/replace.tmp với chế độ write
	if (!file || !fileTemp) {
		printf("Can not open file!\n");
		return 0;
	}

	// Đọc từng dòng trong /etc/shadow
	char line[256];

    while (fgets(line, sizeof(line), file) != NULL) {
        
        if (strstr(line, user) != NULL) { //nếu dòng này chứa user
            		putspent(spwd, fileTemp); // ghi spwd làm định dạng tệp mật khẩu vào /tmp/replace.tmp
            	}
            	else {
            		fputs(line, fileTemp);
            	}
    }

	rename("/tmp/replace.tmp", "/etc/shadow");
	printf("Update Password Successfully !\n");
	// rename("/tmp/replace.tmp", "/etc/shadow"); //đổi tên /tmp/replace.tmp sang /etc/shadow

	fclose(file);
	fclose(fileTemp);
	return 0;
}