-- Copyright (C) 2020  Intel Corporation. All rights reserved.
-- Your use of Intel Corporation's design tools, logic functions 
-- and other software and tools, and any partner logic 
-- functions, and any output files from any of the foregoing 
-- (including device programming or simulation files), and any 
-- associated documentation or information are expressly subject 
-- to the terms and conditions of the Intel Program License 
-- Subscription Agreement, the Intel Quartus Prime License Agreement,
-- the Intel FPGA IP License Agreement, or other applicable license
-- agreement, including, without limitation, that your use is for
-- the sole purpose of programming logic devices manufactured by
-- Intel and sold by Intel or its authorized distributors.  Please
-- refer to the applicable agreement for further details, at
-- https://fpgasoftware.intel.com/eula.

-- PROGRAM		"Quartus Prime"
-- VERSION		"Version 20.1.1 Build 720 11/11/2020 SJ Lite Edition"
-- CREATED		"Thu Jan 06 15:21:19 2022"

LIBRARY ieee;
USE ieee.std_logic_1164.all; 

LIBRARY work;

ENTITY top_level IS 
	PORT
	(
		clk_50MHz :  IN  STD_LOGIC;
		nrst :  IN  STD_LOGIC;
		sine :  IN  STD_LOGIC;
		triangle :  IN  STD_LOGIC;
		square :  IN  STD_LOGIC;
		vga_clk :  OUT  STD_LOGIC;
		vga_sync :  OUT  STD_LOGIC;
		vga_blank :  OUT  STD_LOGIC;
		vga_vs :  OUT  STD_LOGIC;
		vga_hs :  OUT  STD_LOGIC;
		vga_b :  OUT  STD_LOGIC_VECTOR(7 DOWNTO 0);
		vga_g :  OUT  STD_LOGIC_VECTOR(7 DOWNTO 0);
		vga_r :  OUT  STD_LOGIC_VECTOR(7 DOWNTO 0)
	);
END top_level;

ARCHITECTURE bdf_type OF top_level IS 

COMPONENT video_state_machine
	PORT(timing_pins_clk : IN STD_LOGIC;
		 timing_pins_nrst : IN STD_LOGIC;
		 int_inputs_drawn_outputs_sq_o : IN STD_LOGIC;
		 int_inputs_drawn_outputs_sin_o : IN STD_LOGIC;
		 int_inputs_drawn_outputs_tri_o : IN STD_LOGIC;
		 int_inputs_ch_max : IN STD_LOGIC;
		 int_inputs_val_sq : IN STD_LOGIC;
		 int_inputs_val_tri : IN STD_LOGIC;
		 int_inputs_val_sin : IN STD_LOGIC;
		 int_inputs_x_count_top : IN STD_LOGIC;
		 ext_inputs_triangle : IN STD_LOGIC;
		 ext_inputs_sine : IN STD_LOGIC;
		 ext_inputs_square : IN STD_LOGIC;
		 int_outputs_drawn_inputs_clr : OUT STD_LOGIC;
		 int_outputs_drawn_inputs_sq_t : OUT STD_LOGIC;
		 int_outputs_drawn_inputs_tri_t : OUT STD_LOGIC;
		 int_outputs_drawn_inputs_sin_t : OUT STD_LOGIC;
		 int_outputs_clr_x : OUT STD_LOGIC;
		 int_outputs_clr_sin : OUT STD_LOGIC;
		 int_outputs_clr_tri : OUT STD_LOGIC;
		 int_outputs_clr_sq : OUT STD_LOGIC;
		 int_outputs_ch_en : OUT STD_LOGIC;
		 ext_outputs_pixel : OUT STD_LOGIC;
		 ext_outputs_we : OUT STD_LOGIC;
		 int_outputs_sel_output : OUT STD_LOGIC_VECTOR(1 DOWNTO 0)
	);
END COMPONENT;

COMPONENT video_mux
	PORT(A : IN STD_LOGIC_VECTOR(5 DOWNTO 0);
		 B : IN STD_LOGIC_VECTOR(5 DOWNTO 0);
		 C : IN STD_LOGIC_VECTOR(5 DOWNTO 0);
		 sel : IN STD_LOGIC_VECTOR(1 DOWNTO 0);
		 output : OUT STD_LOGIC_VECTOR(5 DOWNTO 0)
	);
END COMPONENT;

COMPONENT vga_top_level
	PORT(ram_module_conc0_din : IN STD_LOGIC;
		 ram_module_conc0_clk : IN STD_LOGIC;
		 ram_module_conc0_we : IN STD_LOGIC;
		 vga_in_nrst : IN STD_LOGIC;
		 vga_in_x_pos : IN STD_LOGIC_VECTOR(6 DOWNTO 0);
		 vga_in_y_pos : IN STD_LOGIC_VECTOR(5 DOWNTO 0);
		 vga_out_vga_clk : OUT STD_LOGIC;
		 vga_out_vga_sync_n : OUT STD_LOGIC;
		 vga_out_vga_blank_n : OUT STD_LOGIC;
		 vga_out_vga_vs : OUT STD_LOGIC;
		 vga_out_vga_hs : OUT STD_LOGIC;
		 vga_out_vga_b : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
		 vga_out_vga_g : OUT STD_LOGIC_VECTOR(7 DOWNTO 0);
		 vga_out_vga_r : OUT STD_LOGIC_VECTOR(7 DOWNTO 0)
	);
END COMPONENT;

COMPONENT sine_generator
	PORT(clk : IN STD_LOGIC;
		 clear : IN STD_LOGIC;
		 dout : OUT STD_LOGIC_VECTOR(5 DOWNTO 0)
	);
END COMPONENT;

COMPONENT triangle_generator
	PORT(clk : IN STD_LOGIC;
		 clear : IN STD_LOGIC;
		 dout : OUT STD_LOGIC_VECTOR(5 DOWNTO 0)
	);
END COMPONENT;

COMPONENT square_generator
	PORT(clk : IN STD_LOGIC;
		 clear : IN STD_LOGIC;
		 dout : OUT STD_LOGIC_VECTOR(5 DOWNTO 0)
	);
END COMPONENT;

COMPONENT gen_offset
	PORT(sin_in : IN STD_LOGIC_VECTOR(5 DOWNTO 0);
		 sq_in : IN STD_LOGIC_VECTOR(5 DOWNTO 0);
		 tri_in : IN STD_LOGIC_VECTOR(5 DOWNTO 0);
		 sin_o : OUT STD_LOGIC_VECTOR(5 DOWNTO 0);
		 sq_o : OUT STD_LOGIC_VECTOR(5 DOWNTO 0);
		 tri_o : OUT STD_LOGIC_VECTOR(5 DOWNTO 0)
	);
END COMPONENT;

COMPONENT drawn_memory
	PORT(clk : IN STD_LOGIC;
		 inputs_clr : IN STD_LOGIC;
		 inputs_sq_t : IN STD_LOGIC;
		 inputs_tri_t : IN STD_LOGIC;
		 inputs_sin_t : IN STD_LOGIC;
		 outputs_sq_o : OUT STD_LOGIC;
		 outputs_sin_o : OUT STD_LOGIC;
		 outputs_tri_o : OUT STD_LOGIC
	);
END COMPONENT;

COMPONENT clock_divider
	PORT(clk_in : IN STD_LOGIC;
		 clk_out : OUT STD_LOGIC
	);
END COMPONENT;

COMPONENT source_selector
	PORT(sel : IN STD_LOGIC;
		 x1 : IN STD_LOGIC_VECTOR(6 DOWNTO 0);
		 x2 : IN STD_LOGIC_VECTOR(6 DOWNTO 0);
		 y1 : IN STD_LOGIC_VECTOR(5 DOWNTO 0);
		 y2 : IN STD_LOGIC_VECTOR(5 DOWNTO 0);
		 x_out : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		 y_out : OUT STD_LOGIC_VECTOR(5 DOWNTO 0)
	);
END COMPONENT;

COMPONENT mod_counter
	PORT(clk : IN STD_LOGIC;
		 en : IN STD_LOGIC;
		 clr : IN STD_LOGIC;
		 top : OUT STD_LOGIC;
		 dout : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)
	);
END COMPONENT;

COMPONENT character_writer
	PORT(clk : IN STD_LOGIC;
		 en : IN STD_LOGIC;
		 max : OUT STD_LOGIC;
		 pixel : OUT STD_LOGIC;
		 x : OUT STD_LOGIC_VECTOR(6 DOWNTO 0);
		 y : OUT STD_LOGIC_VECTOR(5 DOWNTO 0)
	);
END COMPONENT;

COMPONENT position_validator
	PORT(x_pos : IN STD_LOGIC_VECTOR(6 DOWNTO 0);
		 sq : OUT STD_LOGIC;
		 sine : OUT STD_LOGIC;
		 tri : OUT STD_LOGIC
	);
END COMPONENT;

SIGNAL	sm_clr_sin :  STD_LOGIC;
SIGNAL	sm_clr_sq :  STD_LOGIC;
SIGNAL	sm_clr_tri :  STD_LOGIC;
SIGNAL	sm_clr_x :  STD_LOGIC;
SIGNAL	sm_drawn_clr :  STD_LOGIC;
SIGNAL	sm_drawn_sin_t :  STD_LOGIC;
SIGNAL	sm_drawn_sq_t :  STD_LOGIC;
SIGNAL	sm_drawn_tri_t :  STD_LOGIC;
SIGNAL	sm_en_ch :  STD_LOGIC;
SIGNAL	sm_max_ch :  STD_LOGIC;
SIGNAL	sm_pixel :  STD_LOGIC;
SIGNAL	sm_we :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_0 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_1 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_2 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_3 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_4 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_5 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_6 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_7 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_8 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_9 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_10 :  STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_11 :  STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_12 :  STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_13 :  STD_LOGIC_VECTOR(1 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_14 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_15 :  STD_LOGIC_VECTOR(6 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_16 :  STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_17 :  STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_18 :  STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_19 :  STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL	DFF_inst5 :  STD_LOGIC;
SIGNAL	DFF_inst3 :  STD_LOGIC;
SIGNAL	DFF_inst4 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_30 :  STD_LOGIC_VECTOR(6 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_21 :  STD_LOGIC_VECTOR(6 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_22 :  STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_23 :  STD_LOGIC_VECTOR(5 DOWNTO 0);
SIGNAL	SYNTHESIZED_WIRE_24 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_31 :  STD_LOGIC;
SIGNAL	SYNTHESIZED_WIRE_28 :  STD_LOGIC;


BEGIN 
SYNTHESIZED_WIRE_31 <= '1';
SYNTHESIZED_WIRE_28 <= '1';



b2v_inst : video_state_machine
PORT MAP(timing_pins_clk => clk_50MHz,
		 timing_pins_nrst => nrst,
		 int_inputs_drawn_outputs_sq_o => SYNTHESIZED_WIRE_0,
		 int_inputs_drawn_outputs_sin_o => SYNTHESIZED_WIRE_1,
		 int_inputs_drawn_outputs_tri_o => SYNTHESIZED_WIRE_2,
		 int_inputs_ch_max => sm_max_ch,
		 int_inputs_val_sq => SYNTHESIZED_WIRE_3,
		 int_inputs_val_tri => SYNTHESIZED_WIRE_4,
		 int_inputs_val_sin => SYNTHESIZED_WIRE_5,
		 int_inputs_x_count_top => SYNTHESIZED_WIRE_6,
		 ext_inputs_triangle => SYNTHESIZED_WIRE_7,
		 ext_inputs_sine => SYNTHESIZED_WIRE_8,
		 ext_inputs_square => SYNTHESIZED_WIRE_9,
		 int_outputs_drawn_inputs_clr => sm_drawn_clr,
		 int_outputs_drawn_inputs_sq_t => sm_drawn_sq_t,
		 int_outputs_drawn_inputs_tri_t => sm_drawn_tri_t,
		 int_outputs_drawn_inputs_sin_t => sm_drawn_sin_t,
		 int_outputs_clr_x => sm_clr_x,
		 int_outputs_clr_sin => sm_clr_sin,
		 int_outputs_clr_tri => sm_clr_tri,
		 int_outputs_clr_sq => sm_clr_sq,
		 int_outputs_ch_en => sm_en_ch,
		 ext_outputs_pixel => sm_pixel,
		 ext_outputs_we => sm_we,
		 int_outputs_sel_output => SYNTHESIZED_WIRE_13);


b2v_inst1 : video_mux
PORT MAP(A => SYNTHESIZED_WIRE_10,
		 B => SYNTHESIZED_WIRE_11,
		 C => SYNTHESIZED_WIRE_12,
		 sel => SYNTHESIZED_WIRE_13,
		 output => SYNTHESIZED_WIRE_22);


b2v_inst10 : vga_top_level
PORT MAP(ram_module_conc0_din => SYNTHESIZED_WIRE_14,
		 ram_module_conc0_clk => clk_50MHz,
		 ram_module_conc0_we => sm_we,
		 vga_in_nrst => nrst,
		 vga_in_x_pos => SYNTHESIZED_WIRE_15,
		 vga_in_y_pos => SYNTHESIZED_WIRE_16,
		 vga_out_vga_clk => vga_clk,
		 vga_out_vga_sync_n => vga_sync,
		 vga_out_vga_blank_n => vga_blank,
		 vga_out_vga_vs => vga_vs,
		 vga_out_vga_hs => vga_hs,
		 vga_out_vga_b => vga_b,
		 vga_out_vga_g => vga_g,
		 vga_out_vga_r => vga_r);


b2v_inst11 : sine_generator
PORT MAP(clk => clk_50MHz,
		 clear => sm_clr_sin,
		 dout => SYNTHESIZED_WIRE_17);


b2v_inst12 : triangle_generator
PORT MAP(clk => clk_50MHz,
		 clear => sm_clr_tri,
		 dout => SYNTHESIZED_WIRE_19);


b2v_inst13 : square_generator
PORT MAP(clk => clk_50MHz,
		 clear => sm_clr_sq,
		 dout => SYNTHESIZED_WIRE_18);


b2v_inst14 : gen_offset
PORT MAP(sin_in => SYNTHESIZED_WIRE_17,
		 sq_in => SYNTHESIZED_WIRE_18,
		 tri_in => SYNTHESIZED_WIRE_19,
		 sin_o => SYNTHESIZED_WIRE_10,
		 sq_o => SYNTHESIZED_WIRE_12,
		 tri_o => SYNTHESIZED_WIRE_11);


b2v_inst15 : drawn_memory
PORT MAP(clk => clk_50MHz,
		 inputs_clr => sm_drawn_clr,
		 inputs_sq_t => sm_drawn_sq_t,
		 inputs_tri_t => sm_drawn_tri_t,
		 inputs_sin_t => sm_drawn_sin_t,
		 outputs_sq_o => SYNTHESIZED_WIRE_0,
		 outputs_sin_o => SYNTHESIZED_WIRE_1,
		 outputs_tri_o => SYNTHESIZED_WIRE_2);



SYNTHESIZED_WIRE_7 <= NOT(DFF_inst5);



SYNTHESIZED_WIRE_8 <= NOT(DFF_inst3);



SYNTHESIZED_WIRE_9 <= NOT(DFF_inst4);



b2v_inst2 : clock_divider
PORT MAP(clk_in => clk_50MHz);


b2v_inst20 : source_selector
PORT MAP(sel => sm_en_ch,
		 x1 => SYNTHESIZED_WIRE_30,
		 x2 => SYNTHESIZED_WIRE_21,
		 y1 => SYNTHESIZED_WIRE_22,
		 y2 => SYNTHESIZED_WIRE_23,
		 x_out => SYNTHESIZED_WIRE_15,
		 y_out => SYNTHESIZED_WIRE_16);


SYNTHESIZED_WIRE_14 <= SYNTHESIZED_WIRE_24 OR sm_pixel;


PROCESS(clk_50MHz,nrst,SYNTHESIZED_WIRE_31)
BEGIN
IF (nrst = '0') THEN
	DFF_inst3 <= '0';
ELSIF (SYNTHESIZED_WIRE_31 = '0') THEN
	DFF_inst3 <= '1';
ELSIF (RISING_EDGE(clk_50MHz)) THEN
	DFF_inst3 <= sine;
END IF;
END PROCESS;


PROCESS(clk_50MHz,nrst,SYNTHESIZED_WIRE_31)
BEGIN
IF (nrst = '0') THEN
	DFF_inst4 <= '0';
ELSIF (SYNTHESIZED_WIRE_31 = '0') THEN
	DFF_inst4 <= '1';
ELSIF (RISING_EDGE(clk_50MHz)) THEN
	DFF_inst4 <= square;
END IF;
END PROCESS;


PROCESS(clk_50MHz,nrst,SYNTHESIZED_WIRE_31)
BEGIN
IF (nrst = '0') THEN
	DFF_inst5 <= '0';
ELSIF (SYNTHESIZED_WIRE_31 = '0') THEN
	DFF_inst5 <= '1';
ELSIF (RISING_EDGE(clk_50MHz)) THEN
	DFF_inst5 <= triangle;
END IF;
END PROCESS;



b2v_inst7 : mod_counter
PORT MAP(clk => clk_50MHz,
		 en => SYNTHESIZED_WIRE_28,
		 clr => sm_clr_x,
		 top => SYNTHESIZED_WIRE_6,
		 dout => SYNTHESIZED_WIRE_30);


b2v_inst8 : character_writer
PORT MAP(clk => clk_50MHz,
		 en => sm_en_ch,
		 max => sm_max_ch,
		 pixel => SYNTHESIZED_WIRE_24,
		 x => SYNTHESIZED_WIRE_21,
		 y => SYNTHESIZED_WIRE_23);


b2v_inst9 : position_validator
PORT MAP(x_pos => SYNTHESIZED_WIRE_30,
		 sq => SYNTHESIZED_WIRE_3,
		 sine => SYNTHESIZED_WIRE_5,
		 tri => SYNTHESIZED_WIRE_4);


END bdf_type;