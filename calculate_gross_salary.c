/*Calculate Gross Salary of Ramesh*/
/*Author: Anandhavaradhan Pugazhendhi; Date: 31/5/2025*/
#include <stdio.h>
int main()
{
	float bs, da, hra, gs;
	printf("Enter Ramesh's Basic Salary: ");
	scanf("%f", &bs);    /*Basic Salary*/
	da=0.4*bs;           /*Dearness Alowance*/
	hra=0.2*bs;          /*House Rent Allowance*/
	gs=bs+da+hra;        /*Formula for caculating Gross Salary*/
	printf("Ramesh's Gross Salary is %f\n", gs);
	return 0;
}
