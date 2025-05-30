/*Calculate simple interest*/
/*Author Name: Anandhavaradhan; Date: 28/05/2025*/
#include <stdio.h>
int main()
{
	int p, t;
	float r, si;
	/*Formula for simple Interest*/
	si=(p*r*t)/100;
	printf("Calculated interest is ");
	printf("%4.2f\n", si);
	return 0; 
}
