from util.patch.aslr import aslr
COUNT = 3


def patch(pt):

    hello, size = pt.inject(raw='hello world\n', size=True)
    hello += 0x0000555555554000
    print 'hello addr -> ' + hex(hello)

    pt.verbose = True
    addr = pt.inject(asm=r'''
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
    #0x55555595500c
    #addr += 0x0000555555554000
    pt.hook(pt.entry, addr)
