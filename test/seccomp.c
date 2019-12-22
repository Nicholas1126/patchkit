//gcc -g seccomp.c -o seccomp -lseccomp
#include <unistd.h>
#include <seccomp.h>
#include <linux/seccomp.h>
#include <fcntl.h>
int main(void){
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_ALLOW); 

  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(socket), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(connect), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(bind), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(listen), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(clone), 0);  
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0); 
  int fd = open("./bpf.out",O_WRONLY|O_CREAT);
  close(fd);
  seccomp_load(ctx);
  seccomp_export_bpf(ctx,fd);
  system("/bin/sh");
}