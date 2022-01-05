onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -divider timing
add wave -noupdate /top_level/clk_50MHz
add wave -noupdate /top_level/nrst
add wave -noupdate -divider inputs
add wave -noupdate /top_level/sine
add wave -noupdate /top_level/triangle
add wave -noupdate /top_level/square
add wave -noupdate -divider VGA_input
add wave -noupdate -format Analog-Step -height 74 -max 79.0 -radix unsigned /top_level/b2v_inst10/vga_in_x_pos
add wave -noupdate -format Analog-Step -height 74 -max 38.0 -min 20.0 -radix unsigned /top_level/b2v_inst10/vga_in_y_pos
add wave -noupdate /top_level/sm_pixel
add wave -noupdate /top_level/sm_we
add wave -noupdate -divider state_machine
add wave -noupdate /top_level/b2v_inst/n_s
add wave -noupdate /top_level/b2v_inst/p_s
add wave -noupdate /top_level/sm_clr_x
add wave -noupdate -radix unsigned /top_level/b2v_inst/int_inputs_x_count_top
add wave -noupdate -radix unsigned /top_level/b2v_inst1/sel
add wave -noupdate /top_level/b2v_inst/func
add wave -noupdate -divider drawn
add wave -noupdate /top_level/sm_drawn_clr
add wave -noupdate /top_level/sm_drawn_sin_t
add wave -noupdate /top_level/sm_drawn_sq_t
add wave -noupdate /top_level/sm_drawn_tri_t
add wave -noupdate /top_level/b2v_inst15/outputs_tri_o
add wave -noupdate /top_level/b2v_inst15/outputs_sq_o
add wave -noupdate /top_level/b2v_inst15/outputs_sin_o
add wave -noupdate -divider WFG
add wave -noupdate /top_level/sm_clr_sin
add wave -noupdate -format Analog-Step -height 74 -max 14.999999999999998 /top_level/b2v_inst11/dout
add wave -noupdate /top_level/sm_clr_sq
add wave -noupdate -format Analog-Step -height 74 -max 18.0 /top_level/b2v_inst13/dout
add wave -noupdate /top_level/sm_clr_tri
add wave -noupdate -format Analog-Step -height 74 -max 70.0 /top_level/b2v_inst12/dout
add wave -noupdate -divider VGA_output
add wave -noupdate /top_level/vga_clk
add wave -noupdate /top_level/vga_sync
add wave -noupdate /top_level/vga_blank
add wave -noupdate /top_level/vga_vs
add wave -noupdate /top_level/vga_hs
add wave -noupdate /top_level/vga_b
add wave -noupdate /top_level/vga_g
add wave -noupdate /top_level/vga_r
add wave -noupdate -divider counter
add wave -noupdate -format Analog-Step -height 74 -max 79.0 -radix unsigned /top_level/b2v_inst7/counter
add wave -noupdate -divider validator
add wave -noupdate /top_level/b2v_inst9/sq
add wave -noupdate /top_level/b2v_inst9/sine
add wave -noupdate /top_level/b2v_inst9/tri
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {55 ns} 0}
quietly wave cursor active 1
configure wave -namecolwidth 252
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ns
update
WaveRestoreZoom {0 ns} {8204 ns}
