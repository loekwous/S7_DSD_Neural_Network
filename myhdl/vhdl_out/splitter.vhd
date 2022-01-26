-- File: vhdl_out/splitter.vhd
-- Generated by MyHDL 0.11
-- Date: Wed Jan 26 14:01:52 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity splitter is
    port (
        din: in std_logic_vector(9 downto 0);
        a0: out std_logic;
        a1: out std_logic;
        a2: out std_logic;
        a3: out std_logic;
        a4: out std_logic;
        a5: out std_logic;
        a6: out std_logic;
        a7: out std_logic;
        a8: out std_logic;
        a9: out std_logic
    );
end entity splitter;


architecture MyHDL of splitter is



signal din_num: unsigned(9 downto 0);

begin

din_num <= unsigned(din);




a0 <= din_num(0);
a1 <= din_num(1);
a2 <= din_num(2);
a3 <= din_num(3);
a4 <= din_num(4);
a5 <= din_num(5);
a6 <= din_num(6);
a7 <= din_num(7);
a8 <= din_num(8);
a9 <= din_num(9);

end architecture MyHDL;
