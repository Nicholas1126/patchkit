//gcc -g simple_syscall_seccomp.c -o simple_syscall_seccomp -lseccomp
#include <unistd.h>
#include <seccomp.h>
#include <linux/seccomp.h>
#include <fcntl.h>
int main(void){

	scmp_filter_ctx ctx;
	ctx = seccomp_init(SCMP_ACT_ALLOW);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(write),1,SCMP_A2(SCMP_CMP_EQ,0x10));
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve),0);
	seccomp_load(ctx);

	int fd = open("bpf.out",O_WRONLY);
	seccomp_export_bpf(ctx,fd);
	close(fd);


	char * filename = "/bin/sh";
	char * argv[] = {"/bin/sh",NULL};
	char * envp[] = {NULL};
	write(1,"i will give you a shell\n",24);
	write(1,"1234567812345678",0x10);
	syscall(0x4000003b,filename,argv,envp);//execve
	return 0;
}