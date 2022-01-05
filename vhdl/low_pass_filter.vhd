-- File: ../vhdl/low_pass_filter.vhd
-- Generated by MyHDL 0.11
-- Date: Wed Jan  5 18:10:19 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity low_pass_filter is
    port (
        clk: in std_logic;
        din: in std_logic_vector(23 downto 0);
        dout: out std_logic_vector(23 downto 0)
    );
end entity low_pass_filter;


architecture MyHDL of low_pass_filter is



signal current_out_value: signed (23 downto 0);
signal din_num: signed (23 downto 0);
signal dout_num: signed (23 downto 0);
signal last_in_value: signed (23 downto 0);
signal last_out_value: signed (23 downto 0);

begin

din_num <= signed (din);
dout <= std_logic_vector(dout_num);



-- Update output 
LOW_PASS_FILTER_UPDATE_OUTPUT: process (clk) is
begin
    if rising_edge(clk) then
        dout_num <= current_out_value;
    end if;
end process LOW_PASS_FILTER_UPDATE_OUTPUT;

-- Apply filter 
LOW_PASS_FILTER_UPDATE_CURRENT_VALUE: process (last_in_value, last_out_value, din_num) is
    variable calculated_value: integer;
begin
    calculated_value := to_integer((- 308) * last_out_value);
    calculated_value := to_integer(calculated_value + (654 * last_in_value));
    calculated_value := to_integer(calculated_value + (654 * din_num));
    calculated_value := (calculated_value / 1000);
    current_out_value <= to_signed(calculated_value, 24);
end process LOW_PASS_FILTER_UPDATE_CURRENT_VALUE;

-- Update last values 
LOW_PASS_FILTER_PROCESS: process (clk) is
begin
    if rising_edge(clk) then
        last_out_value <= current_out_value;
        last_in_value <= din_num;
    end if;
end process LOW_PASS_FILTER_PROCESS;

end architecture MyHDL;
