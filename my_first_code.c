/*Calculate simple interest*/
/*Author Name: Anandhavaradhan; Date: 28/05/2025*/
#include <stdio.h>
int main()
{
	int p, t;
	float r, si;
	p=5000;
	r=5;
	t=3;	
	si=(p*r*t)/100;    /*Formula for simple Interest*/
	printf("Calculated interest is ");
	printf("%4.2f\n", si);
	return 0; 
}
