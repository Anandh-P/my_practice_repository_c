/*Calculation of simple interest*/
/*Author: Anandhavaradhan Pugazhendhi; Date: 30/5/2025*/
#include <stdio.h>
int main()
{
	int p,t;
	float r,si,atbp;
	printf("Enter the values of the principle, rate, and number of years: ");
	scanf("%d %d %f", &p, &t, &r);
	si = (p*r*t)/100;   /*Formula for simple interest*/
	atbp = si+p;        /*To calculate total amount to be paid*/
	printf("You have to pay ");
	printf("%f\n",atbp);
	return 0;
}
