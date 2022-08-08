% Use this editor as a MiniZinc scratch book
int: n; %numero de ciudades
int: m;
array[1..m,1..2] of int : c; %ubicacion de las ciudades 
var int: pos;
var 0..n: x;
var 0..n: y;
var 0..m: far;
constraint pos = abs(c[far,1]-x)+abs(c[far,2]-y);
constraint x >= 0 /\ x <= n;
constraint y >= 0 /\ y <= n;
constraint forall (i in 1..m) (x!=c[i,1] \/ y!=c[i,2]);
constraint forall (i in 1..m) (abs(c[i,1]-x)+abs(c[i,2]-y) <= abs(c[far,1]-x)+abs(c[far,2]-y));


solve minimize pos;

output[ show(x)," ",show(y)," ", show(pos) ,"  ", show(c[far,1]),",",show(c[far,2]) ];