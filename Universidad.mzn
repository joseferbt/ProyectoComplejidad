% Use this editor as a MiniZinc scratch book
int: n; %numero de ciudades
int: m;
array[1..m,1..2] of int : c; %ubicacion de las ciudades 
var int: pos;
var 0.0..n: x;
var 0.0..n: y;

constraint pos = sum(j in 1..m)(abs(c[j,1]-x)+abs(c[j,2]-y));


solve minimize pos;

output[ " x=",show(x),"\n y=",show(y),"\n distance=" , show (pos)];