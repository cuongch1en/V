#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pwd.h>
#include <grp.h>
#include <unistd.h>

#define MAX_GROUPS 100

void get_user_info(const char *username) {
//getpwnam(username) tìm kiếm thông tin người dùng trong /etc/passwd
// Nếu tìm thấy trả về con trỏ struct passwd chứa thông tin người dùng
// Dữ liệu có thể truy cập thông qua các trường như: pw_uid, pw_name, pw_dir
    struct passwd *pw = getpwnam(username);
    if (!pw) {
        printf("User not found.\n");
        return;
    }
    
    printf("User ID: %d\n", pw->pw_uid);
    printf("Username: %s\n", pw->pw_name);
    printf("Home Directory: %s\n", pw->pw_dir);
    
    // Lấy danh sách nhóm
    // gid_t là kiểu số nguyên đại diện cho GroupID, được khai trong <unistd.h>
    gid_t groups[MAX_GROUPS];
    int ngroups = MAX_GROUPS;
    struct group *gr;
//getgrouplist() tìm danh sách nhóm của người dùng từ tệp /etc/group.
// Lưu danh sách GID của nhóm vào mảng groups
// & ngroups trả về số nhóm thực tế mà người dugf thuộc vào
    if (getgrouplist(username, pw->pw_gid, groups, &ngroups) == -1) {
        printf("Error getting groups.\n");
        return;
    }
    
    printf("Groups: ");
    for (int i = 0; i < ngroups; i++) {
        gr = getgrgid(groups[i]);
        if (gr) {
            printf("%s%s", gr->gr_name, (i < ngroups - 1) ? ", " : "\n");
        }
    }
}

int main() {
    char username[98];
    
    printf("Enter username: ");
    if (scanf("%s", username) != 1) {
        printf("Invalid input.\n");
        return 1;
    }
    
    get_user_info(username);
    return 0;
}