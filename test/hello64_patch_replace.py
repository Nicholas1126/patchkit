def replace_add(pt):
    pt.verbose = True
    add_addr = 0x64A
    new_addr = pt.inject(c=r'''
    int add(int a, int b)
    {
        return b-a;
    }
    ''')
    print ("jmp %s" % (hex(new_addr)))
    pt.patch(add_addr, asm=("jmp %s" % (hex(new_addr))))

""" def replace_add(pt):
    pt.verbose = True
    add_addr = 0x64A

    pt.patch(add_addr, c=r'''
    int add(int a, int b)
    {
        return b-a;
    }
    ''')
 """
    