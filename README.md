新脚本:
----
- 先将hpwnwaf.py 中 main_addr 改为需要修改的二进制文件中main函数入口地址,然后执行```./patch ELF hpwnwaf.py``` 
- 暂时只支持linux 64位程序


- hpwnwaf 中的过滤规则为 
``` 
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_ALLOW);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(socket), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(connect), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(bind), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(listen), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(clone), 0);  
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0); 
```
- hpwnwaf2中的过滤规则为 
```
  scmp_filter_ctx ctx;
  ctx = seccomp_init(SCMP_ACT_ALLOW);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(bind), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(listen), 0);
  seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0); 
```

- test目录下的源码可构建通防策略的二进制，根据需要ban掉函数，然后使用patch进行打补丁：
```
def replace_waf(pt):
	main_addr = pt.entry #main函数入口地址
	new_main = pt.inject(asm=r'''
	push rbp;
	mov rbp,rsp;
	mov r15,6;
	push r15;
	mov r15,7FFF000000000006H;
	push r15;	
	mov r15,3B00010015H;
	push r15;
	mov r15 , 3800020015h;
	push r15;
	mov r15 , 3200030015h;
	push r15;
	mov r15 , 3100040015h;
	push r15;
	mov r15 , 2A00050015h;
	push r15;
	mov r15 , 2900060015h;
	push r15;
	mov r15 , 4000000000070035h;
	push r15;
	mov r15 , 20h;
	push r15;
	mov r15 , 0C000003E09000015h;
	push r15;
	mov r15 , 400000020h;
	push r15;
	mov r15,rsp;
	push r15;
	mov r15 , 0ch;
	push r15;
	mov r15,rsp;	
	push r15;
	mov rdi,38;
	mov rsi,1;
	mov rdx,0;
	mov rcx,0;
	mov r8,0;
	mov rax,157;
	syscall;
	mov rdi,22;
	mov rsi,2;
	mov rdx,r15;
	mov rax,157;
	syscall;
	leave;	
	ret;
	''')
	pt.hook(main_addr, new_main)
```


新特性：
----
- 新增patchblock功能，实现对起始地址到结束地址的patch：
  - 当需要asm代码的长度比原始二进制的长度小时，支持使用fill字段填充任意值（patch接口也同步做了优化）例如：
    ```
    pt.patch(0x000000000000094F, asm=
    '''ret''', 
    desc='patchblock', fill='\x90')
    ```
  - 当需要asm代码的长度比原始二进制的长度大时，空间不足而失败。
说明：实现patchblock的目的是patch接口对于即将要patch的指令机器码小于原始机器码的情况处理不好，第一个是不能自动填充补齐，第二个是调用self.dis接口依赖于长度值，长度值不对的话解析指令机器码错误，故实现目的减去源地址，从而规避此问题。

- 新增hook_inline功能，原来的hook功能实现不清晰，重新实现了一个函数，使用可参考：
    ```def hook_fsb(pt):
        pt.verbose = True
        fsb_addr = 0x0000000000000C00
        hook_addr = pt.inject(asm=r'''
        mov rsi, rdi
        push 0x0a0d7325
        mov rdi, rsp
        add rsp, 8
        ret
        ''')
        pt.hook_inline(fsb_addr, hook_addr)```

更多使用待续...