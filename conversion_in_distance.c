/*Conversion in Distance*/
/*Author: Anandhavaradhan; Date:1/6/2025*/
#include <stdio.h>
int main()
{
	float km, m, f, in, cm;
	printf("Enter value in Kilometers: ");
	scanf("%f", &km);
	m = 1000*km;
	f = 3280.84*km;
	in = 39370.1*km;
	cm = 100000*km;
	printf("Distance in Meters is %f\n", m);
	printf("Distance in Feet is %f\n", f);
	printf("Distance in Inches is %f\n", in);
	printf("Distance in Centimeters is %f\n", cm);
	return 0;
}
