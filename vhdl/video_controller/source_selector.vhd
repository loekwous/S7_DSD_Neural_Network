-- File: ../vhdl/video_controller/source_selector.vhd
-- Generated by MyHDL 0.11
-- Date: Thu Jan  6 14:50:07 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity source_selector is
    port (
        sel: in std_logic;
        x1: in std_logic_vector(6 downto 0);
        y1: in std_logic_vector(5 downto 0);
        x2: in std_logic_vector(6 downto 0);
        y2: in std_logic_vector(5 downto 0);
        x_out: out std_logic_vector(6 downto 0);
        y_out: out std_logic_vector(5 downto 0)
    );
end entity source_selector;


architecture MyHDL of source_selector is



signal x1_num: unsigned(6 downto 0);
signal x2_num: unsigned(6 downto 0);
signal x_out_num: unsigned(6 downto 0);
signal y1_num: unsigned(5 downto 0);
signal y2_num: unsigned(5 downto 0);
signal y_out_num: unsigned(5 downto 0);

begin

x1_num <= unsigned(x1);
y1_num <= unsigned(y1);
x2_num <= unsigned(x2);
y2_num <= unsigned(y2);
x_out <= std_logic_vector(x_out_num);
y_out <= std_logic_vector(y_out_num);



SOURCE_SELECTOR_OUTPUT_CONTROL: process (y2_num, x1_num, y1_num, sel, x2_num) is
begin
    if (sel = '1') then
        x_out_num <= x2_num;
        y_out_num <= y2_num;
    else
        x_out_num <= x1_num;
        y_out_num <= y1_num;
    end if;
end process SOURCE_SELECTOR_OUTPUT_CONTROL;

end architecture MyHDL;