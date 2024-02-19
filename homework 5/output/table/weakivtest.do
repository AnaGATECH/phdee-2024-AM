sjlog using weakivtest1,replace
use data_usaq
qui ivreg2 dc (rrf=z1 z2 z3 z4), robust bw(7)
weakivtest
sjlog close, replace
