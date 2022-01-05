restart -f

force clk_50MHz 0 0, 1 10 -r 20
force nrst 1 0, 0 35, 1 55
force sine 1 0, 0 5000, 1 10000
force triangle 1 0, 0 15000, 1 20000
force square 1 0, 0 25000, 1 30000

run 1000000