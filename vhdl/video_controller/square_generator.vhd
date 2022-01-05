-- File: ../vhdl/video_controller/square_generator.vhd
-- Generated by MyHDL 0.11
-- Date: Wed Jan  5 13:25:55 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity square_generator is
    port (
        clk: in std_logic;
        clear: in std_logic;
        dout: out std_logic_vector(5 downto 0)
    );
end entity square_generator;


architecture MyHDL of square_generator is



signal counter: unsigned(4 downto 0);
signal dout_num: unsigned(5 downto 0);

begin

dout <= std_logic_vector(dout_num);



SQUARE_GENERATOR_COUNTING_MANAGEMENT: process (clk) is
begin
    if rising_edge(clk) then
        if (clear = '1') then
            counter <= to_unsigned(0, 5);
        else
            if (signed(resize(counter, 6)) < (25 - 1)) then
                counter <= (counter + 1);
            else
                counter <= to_unsigned(0, 5);
            end if;
        end if;
    end if;
end process SQUARE_GENERATOR_COUNTING_MANAGEMENT;

SQUARE_GENERATOR_SIGNAL_GENERATOR: process (counter) is
begin
    case to_integer(counter) is
        when 0 => dout_num <= "000000";
        when 1 => dout_num <= "000111";
        when 2 => dout_num <= "001110";
        when 3 => dout_num <= "010101";
        when 4 => dout_num <= "011100";
        when 5 => dout_num <= "100011";
        when 6 => dout_num <= "101011";
        when 7 => dout_num <= "101011";
        when 8 => dout_num <= "101011";
        when 9 => dout_num <= "101011";
        when 10 => dout_num <= "101011";
        when 11 => dout_num <= "101011";
        when 12 => dout_num <= "101011";
        when 13 => dout_num <= "101011";
        when 14 => dout_num <= "101011";
        when 15 => dout_num <= "101011";
        when 16 => dout_num <= "101011";
        when 17 => dout_num <= "101011";
        when 18 => dout_num <= "101011";
        when 19 => dout_num <= "101001";
        when 20 => dout_num <= "100010";
        when 21 => dout_num <= "011010";
        when 22 => dout_num <= "010011";
        when 23 => dout_num <= "001100";
        when others => dout_num <= "000101";
    end case;
end process SQUARE_GENERATOR_SIGNAL_GENERATOR;

end architecture MyHDL;
