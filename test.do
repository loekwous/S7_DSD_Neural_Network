restart -f

force clk 0 0, 1 10 -r 20
force nrst 1 1, 0 50, 1 100
force we 0 0, 1 200, 0 215

force x_pos 10#10
force y_pos 10#20
force pixel 0

run 22000000
