library ieee;
use ieee.std_logic_1164.all; 
use ieee.std_logic_arith.all; 

entity tb_audio_decoder is 
end entity tb_audio_decoder;

architecture tb of tb_audio_decoder is
	component audio_decoder
	port(
			clk_i2s :  in  STD_LOGIC := '0';
			adc_data :  in  STD_LOGIC := '0';
			enable_decoder :  in  STD_LOGIC := '0';
			nrst :  in  STD_LOGIC := '1';
			adclrc :  out  STD_LOGIC;
			data_ready :  out  STD_LOGIC;
			dout :  out  STD_LOGIC_VECTOR(47 downto 0)
		);
	end component; 

	constant T : time := 100 ns; 
	
	signal tb_clk_i2s, tb_adc_data, tb_enable_decoder, tb_nrst: std_logic; -- input
	signal tb_adclrc, tb_data_ready: std_logic; -- output
	signal tb_dout: std_logic_vector(47 downto 0); -- output
	signal test_succesfull: std_logic; -- test variable
	signal counter: integer:= 0; 
	
begin
	
	DUT: audio_decoder
	port map (
		clk_i2s			=> tb_clk_i2s, 
		adc_data 		=> tb_adc_data,
		enable_decoder => tb_enable_decoder, 
		nrst 				=> tb_nrst, 
		adclrc 			=> tb_adclrc, 
		data_ready 		=> tb_data_ready, 
		dout 				=> tb_dout
	);
	
	clk: process -- Clock signal
	begin	
		tb_clk_i2s <= '0';
		wait for T/2; 
		tb_clk_i2s <= '1'; 
		wait for T/2; 	
	end process; 
	
	testSequance: process -- Test sequance
	begin
		tb_nrst <= '1'; -- set start values
		tb_enable_decoder <= '0'; 
		tb_adc_data <= '0'; 
		wait for T; 
		
		tb_nrst <= '0'; -- reset controller
		tb_enable_decoder <= '0'; 
		tb_adc_data <= '0'; 
		wait for T; 
		
		tb_nrst <= '1'; -- wait a clock cycle 
		tb_enable_decoder <= '0'; 
		tb_adc_data <= '0'; 
		wait for T*2; 
		
		tb_nrst <= '1'; -- enable controller
		tb_enable_decoder <= '1'; 
		tb_adc_data <= '0'; 
		wait for T; 
		
		tb_nrst <= '1'; -- wait a clock cycle
		tb_enable_decoder <= '1'; 
		tb_adc_data <= '0'; 
		wait for T; 
		
		while counter /= 24  loop
			tb_nrst <= '1'; -- wait a clock cycle
			tb_enable_decoder <= '1'; 
			tb_adc_data <= not tb_adc_data; 
			wait for T; 
			counter <= counter + 1; 
		end loop; 
		
		tb_nrst <= '1'; -- wait a clock cycle
		tb_enable_decoder <= '1'; 
		tb_adc_data <= '0'; 
		wait for T;
		
		while counter /= 24  loop
			tb_nrst <= '1'; -- wait a clock cycle
			tb_enable_decoder <= '1'; 
			tb_adc_data <= not tb_adc_data; 
			wait for T; 
			counter <= counter + 1; 
		end loop; 
		
		wait for 300 ns;
	end process;
	
	check: process -- Check output
	begin 
		if tb_data_ready = '1' then
			if tb_dout = "000010101010101010101010010101010101010101010101" then 
				-- Test succesfull 
				test_succesfull <= '1';
				wait;
			end if;
			
		else 
			test_succesfull <= '0';	 
		end if;
		wait for T;
	end process; 

end tb;
