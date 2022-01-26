-- File: ../vhdl/neural_network\threshold_detector.vhd
-- Generated by MyHDL 0.11
-- Date: Sun Jan  9 14:42:03 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity threshold_detector is
    port (
        in0: in std_logic_vector(32 downto 0);
        in1: in std_logic_vector(32 downto 0);
        in2: in std_logic_vector(32 downto 0);
        out0: out std_logic;
        out1: out std_logic;
        out2: out std_logic
    );
end entity threshold_detector;


architecture MyHDL of threshold_detector is



signal in0_num: signed (32 downto 0);
signal in1_num: signed (32 downto 0);
signal in2_num: signed (32 downto 0);

begin

in0_num <= signed (in0);
in1_num <= signed (in1);
in2_num <= signed (in2);



THRESHOLD_DETECTOR_LOGIC: process (in0_num, in2_num, in1_num) is
    variable exact_half: integer;
begin
    exact_half := (1024 / 2);
    out0 <= tern_op(cond => (in0_num > exact_half), if_true => '1', if_false => '0');
    out1 <= tern_op(cond => (in1_num > exact_half), if_true => '1', if_false => '0');
    out2 <= tern_op(cond => (in2_num > exact_half), if_true => '1', if_false => '0');
end process THRESHOLD_DETECTOR_LOGIC;

end architecture MyHDL;
