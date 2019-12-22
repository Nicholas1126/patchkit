//gcc -g hpwnwaf.c -o hpwnwaf
#include <stdio.h>

int main(void){

	printf("i will give you a shell\n");
    system("/bin/sh");
	return 0;
}