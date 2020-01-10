#def hook_fsb(pt):
#    pt.verbose = True
#    fsb_addr = 0x0000000000000C00
#    hook_addr = pt.inject(asm=r'''
#    mov rsi, rdi
#    push 0x0a0d7325
#    mov rdi, rsp
#    add rsp, 8
#    ret
#    ''')

def hook_add(pt):
    pt.verbose = True
    ASLR = 0x0000555555554000
    hello, size = pt.inject(raw='hello world\n', size=True)
    print hex(hello)
    #hello += ASLR

    add_addr = 0x64A
    hook_addr = pt.inject(asm=r'''
    push rax
    push rdi
    push rsi
    push rdx

    mov rax, 1  # SYS_write
    mov rdi, 1  # fd
    mov rsi, %d # buf
    mov rdx, %d # size
    syscall

    pop rdx
    pop rsi
    pop rdi
    pop rax
    ret
    ''' % (hello, size))
    
    pt.hook_inline(add_addr, hook_addr)
