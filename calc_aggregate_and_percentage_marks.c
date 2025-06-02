/*Calculation of Aggregate and Percentage marks*/
/*Author: Anandhavaradhan; Date:2/6/2025*/
#include <stdio.h>
int main()
{
	int m1, m2, m3, m4, m5, aggr;
	float per;
	printf("\nEnter the marks of 5 Subjects(Eg: 97, 84, 86, 96, 91): ");
	scanf ("%d, %d, %d, %d, %d", &m1, &m2, &m3, &m4, &m5);
	aggr = m1+m2+m3+m4+m5;
	per = aggr/5;
	printf("The Aggregate of the given Marks is %d\n", aggr);
	printf("The Percentage Marks of the given Marks is %f\n", per);
	return 0;
}
