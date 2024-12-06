#include <stdio.h>

int main(void){
int resultado = 1;
for(int i = 0; i < 3; i++){
resultado *= 2;
}

printf("%d\n", resultado);
}