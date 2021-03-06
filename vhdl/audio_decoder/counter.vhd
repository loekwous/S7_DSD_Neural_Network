-- File: counter.vhd
-- Generated by MyHDL 0.11
-- Date: Tue Jan  4 17:19:12 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;


entity counter is
    port (
        clk: 		in std_logic;
        cntr_en: 	in std_logic;
		  clr:		in std_logic;
        half: 		out std_logic;
        top: 		out std_logic
    );
end entity counter;


architecture MyHDL of counter is



signal counter: unsigned(5 downto 0);

begin

COUNTER_UPDATE_COMB: process (counter) is
begin
    if (counter = 24) then
        half <= '1' after 5 ns;
    else
        half <= '0' after 5 ns;
    end if;
    if (counter = 48) then
        top <= '1' after 5 ns;
    else
        top <= '0' after 5 ns;
    end if;
end process COUNTER_UPDATE_COMB;

COUNTER_UPDATE: process (clk) is
begin
    if rising_edge(clk) then
		  if (clr = '1') then 
				counter <= (others=> '0') after 5 ns;
        elsif (cntr_en = '1') then
            counter <= unsigned(counter) + 1 after 5 ns;
		  end if; 
    end if;
end process COUNTER_UPDATE;

end architecture MyHDL;
