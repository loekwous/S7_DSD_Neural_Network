restart -f

force clk 0 0, 1 10 -r 20
force clr 0 0, 1 25, 0 35
force en 0 0, 1 45, 0 115
force data 10#0 0, 10#1024 45, 10#2048 65, 10#4096 85, 10#8192 105, 10#0 125
force funct 10#0 0, 10#1 85, 10#0 125
force sel 10#0 0, 10#1 65, 10#0 85, 10#1 105
run 140