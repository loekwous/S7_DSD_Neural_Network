library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity audio_decoder_controller is 
port (
	clk_i2s		: in std_logic; -- at most 4.6MHz 
	adc_data		: in std_logic; 
	enable		: in std_logic;
	nrst			: in std_logic;
	
	-- counter intputs
	cntr_halfway: in std_logic; 
	cntr_done	: in std_logic;
	
	--data_out		: out std_logic_vector(47 downto 0); -- will be in the sipo block
	bclk			: out std_logic; 
	adclrc		: out std_logic;
	
	-- counter outputs 
	cntr_en 		: out std_logic; 
	cntr_clear 	: out std_logic;
	
	-- sipo inputs
	data_ready	: out std_logic;
	data_out		: out std_logic; 
	sipo_en		: out std_logic;
	sipo_clear	: out std_logic
	
);
end audio_decoder_controller;

architecture controller of audio_decoder_controller is

type state is (s0, s1, s2, s3, s4, s5, s6); 
signal next_state		: state; 
signal present_state	: state;

begin
		
	-- next state decoder
	next_state_dec_proc:
	process(present_state, enable, cntr_halfway, cntr_done)
		variable n_s : state;
	begin
		case present_state is
			when s0 => 
				if enable = '1' then 
					n_s := s1;
				else
					n_s := s0;
				end if; 
	
			when s1 => -- state 1
				n_s := s2;
				
			when s2 => -- state 2
				if cntr_halfway = '1' then 
					n_s := s3;
				else
					n_s := s2;
				end if; 

			when s3 => -- state 3
				n_s := s4;
			
			when s4 => -- state 4
				if cntr_done = '1' then 
					n_s := s5;
				else
					n_s := s4;
				end if; 
			
			when s5 => -- state 5
				n_s := s6; 
			
			when s6 => -- state 6
				n_s := s1; 
				
			
			when others => NULL; -- something went wrong
		end case; 
		next_state <= n_s after 5 ns;
	end process;
	
	
	-- memory
	mem_proc:
	process(nrst, clk_i2s)
	begin
		if nrst = '0' then
			present_state <= s6; 
		elsif rising_edge(clk_i2s) then
			present_state <= next_state; 
		end if; 
	end process;
	
	-- output decoder
	output_dec_proc:
	process(present_state, clk_i2s, adc_data)
	begin
		case present_state is 
			when s0 => -- state 0 -- standby state
				-- controller outputs 
				data_ready	<= '0' after 5 ns;
				bclk			<= '0' after 5 ns;
				adclrc		<= '0' after 5 ns;
				-- counter outputs 
				cntr_en 		<= '0' after 5 ns;
				cntr_clear 	<= '0' after 5 ns;
				-- sipo inputs
				sipo_en		<= '0' after 5 ns;
				data_out		<= '0' after 5 ns;
				sipo_clear	<=	'0' after 5 ns;			
				
			when s1 => -- state 1 --wait first clock cycle while pulling adclrc line low
				-- controller outputs
				data_ready	<= '0' after 5 ns;
				bclk			<= not clk_i2s after 5 ns;
				adclrc		<= '0' after 5 ns;
				-- counter outputs 
				cntr_en 		<= '0' after 5 ns;
				cntr_clear 	<= '0' after 5 ns;
				-- sipo inputs
				sipo_en		<= '0' after 5 ns;
				data_out		<= '0' after 5 ns;
				sipo_clear	<=	'0' after 5 ns;		
			
			when s2 => -- state 2 -- read left channel data 
				-- controller outputs
				data_ready	<= '0' after 5 ns;
				bclk			<= not clk_i2s after 5 ns;
				adclrc		<= '0' after 5 ns;
				-- counter outputs 
				cntr_en 		<= '1' after 5 ns;
				cntr_clear 	<= '0' after 5 ns;
				-- sipo inputs
				sipo_en		<= '1' after 5 ns;
				data_out		<= adc_data after 5 ns;
				sipo_clear	<=	'0' after 5 ns;		
			
			when s3 => -- state 3 -- wait clock cycle while turning adclrc line high
				-- controller outputs
				data_ready	<= '0' after 5 ns;
				bclk			<= not clk_i2s after 5 ns;
				adclrc		<= '1' after 5 ns;
				-- counter outputs 
				cntr_en 		<= '0' after 5 ns;
				cntr_clear 	<= '0' after 5 ns;
				-- sipo inputs
				sipo_en		<= '0' after 5 ns;
				data_out		<= '0' after 5 ns;
				sipo_clear	<=	'0' after 5 ns;		
			
			when s4 => -- state 4 -- read right channel data
				-- controller outputs
				data_ready	<= '0' after 5 ns;
				bclk			<= not clk_i2s after 5 ns;
				adclrc		<= '1' after 5 ns;
				-- counter outputs 
				cntr_en 		<= '1' after 5 ns;
				cntr_clear 	<= '0' after 5 ns;
				-- sipo inputs
				sipo_en		<= '1' after 5 ns;
				data_out		<= adc_data after 5 ns;
				sipo_clear	<=	'0' after 5 ns;
		
			when s5 => -- state 5 -- output data ready, wait a clock cycle
				-- controller outputs
				data_ready	<= '1' after 5 ns;
				bclk			<= not clk_i2s after 5 ns;
				adclrc		<= '1' after 5 ns;
				-- counter outputs 
				cntr_en 		<= '0' after 5 ns;
				cntr_clear 	<= '0' after 5 ns;
				-- sipo inputs
				sipo_en		<= '0' after 5 ns;
				data_out		<= '0' after 5 ns;
				sipo_clear	<=	'0' after 5 ns;
				
			when s6 => -- state 6 -- reset counter and sipo and start cycle again
				-- controller outputs
				data_ready	<= '0' after 5 ns;
				bclk			<= not clk_i2s after 5 ns;
				adclrc		<= '1' after 5 ns;
				-- counter outputs 
				cntr_en 		<= '0' after 5 ns;
				cntr_clear 	<= '1' after 5 ns;
				-- sipo inputs
				sipo_en		<= '0' after 5 ns;
				data_out		<= '0' after 5 ns;
				sipo_clear	<=	'1' after 5 ns;		
				
			when others => NULL; -- something went wrong
				data_ready	<= 'X' after 5 ns;
				bclk			<= 'X' after 5 ns;
				adclrc		<= 'X' after 5 ns;
				-- counter outputs 
				cntr_en 		<= 'X' after 5 ns;
				cntr_clear 	<= 'X' after 5 ns;
				-- sipo inputs
				sipo_en		<= 'X' after 5 ns;
				data_out		<= 'X' after 5 ns;
				sipo_clear	<=	'X' after 5 ns;		
		end case; 
	end process; 
	 
end architecture; 