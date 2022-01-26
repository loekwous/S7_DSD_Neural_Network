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
-- CREATED		"Sat Jan 15 16:33:28 2022"

LIBRARY ieee;
USE ieee.std_logic_1164.all; 

LIBRARY work;

ENTITY audio_decoder IS 
	PORT
	(
		clk_i2s :  IN  STD_LOGIC;
		adc_data :  IN  STD_LOGIC;
		enable_decoder :  IN  STD_LOGIC;
		nrst :  IN  STD_LOGIC;
		adclrc :  OUT  STD_LOGIC;
		data_ready :  OUT  STD_LOGIC;
		dout :  OUT  STD_LOGIC_VECTOR(47 DOWNTO 0)
	);
END audio_decoder;

ARCHITECTURE bdf_type OF audio_decoder IS 

COMPONENT audio_decoder_controller
	PORT(clk_i2s : IN STD_LOGIC;
		 adc_data : IN STD_LOGIC;
		 enable : IN STD_LOGIC;
		 nrst : IN STD_LOGIC;
		 cntr_halfway : IN STD_LOGIC;
		 cntr_done : IN STD_LOGIC;
		 bclk : OUT STD_LOGIC;
		 adclrc : OUT STD_LOGIC;
		 cntr_en : OUT STD_LOGIC;
		 cntr_clear : OUT STD_LOGIC;
		 data_ready : OUT STD_LOGIC;
		 data_out : OUT STD_LOGIC;
		 sipo_en : OUT STD_LOGIC;
		 sipo_clear : OUT STD_LOGIC
	);
END COMPONENT;

COMPONENT sipo
	PORT(clk : IN STD_LOGIC;
		 clr : IN STD_LOGIC;
		 sipo_en : IN STD_LOGIC;
		 din : IN STD_LOGIC;
		 dout : OUT STD_LOGIC_VECTOR(47 DOWNTO 0)
	);
END COMPONENT;

COMPONENT counter
	PORT(clk : IN STD_LOGIC;
		 cntr_en : IN STD_LOGIC;
		 clr : IN STD_LOGIC;
		 half : OUT STD_LOGIC;
		 top : OUT STD_LOGIC
	);
END COMPONENT;

SIGNAL	bclk :  STD_LOGIC;
SIGNAL	cntr_clear :  STD_LOGIC;
SIGNAL	cntr_done :  STD_LOGIC;
SIGNAL	cntr_en :  STD_LOGIC;
SIGNAL	cntr_halfway :  STD_LOGIC;
SIGNAL	data :  STD_LOGIC;
SIGNAL	sipo_clear :  STD_LOGIC;
SIGNAL	sipo_en :  STD_LOGIC;


BEGIN 



b2v_inst : audio_decoder_controller
PORT MAP(clk_i2s => clk_i2s,
		 adc_data => adc_data,
		 enable => enable_decoder,
		 nrst => nrst,
		 cntr_halfway => cntr_halfway,
		 cntr_done => cntr_done,
		 bclk => bclk,
		 adclrc => adclrc,
		 cntr_en => cntr_en,
		 cntr_clear => cntr_clear,
		 data_ready => data_ready,
		 data_out => data,
		 sipo_en => sipo_en,
		 sipo_clear => sipo_clear);


b2v_inst2 : sipo
PORT MAP(clk => bclk,
		 clr => sipo_clear,
		 sipo_en => sipo_en,
		 din => data,
		 dout => dout);


b2v_inst3 : counter
PORT MAP(clk => bclk,
		 cntr_en => cntr_en,
		 clr => cntr_clear,
		 half => cntr_halfway,
		 top => cntr_done);


END bdf_type;