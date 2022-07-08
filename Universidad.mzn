% Use this editor as a MiniZinc scratch book
int: n; %numero de ciudades
array[int ,int] of int : c; %ubicacion de las ciudades 
var int: pos;
var int: x;
var int: y;
array[1..n] of var bool: X;
/*
var float: x;
var float: y;
constraint x <= n;
constraint y <= n;
constraint pos = sum(j in 1..n)(sqrt(abs(c[j,1]-x)+abs(c[j,2]-y)));
*/
constraint x >= 0;
constraint y >= 0;
constraint pos = sum(j in 1..n)(X[j]*(c[j,1]+c[j,2]));
constraint 1 = sum(i in 1..n)(X[i]);

solve maximize pos;

output[ show(x),"\n utilidad=" , show (pos)];