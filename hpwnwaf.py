#coding:utf-8
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