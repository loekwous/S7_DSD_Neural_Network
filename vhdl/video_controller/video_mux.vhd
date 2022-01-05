-- File: ../vhdl/video_controller/video_mux.vhd
-- Generated by MyHDL 0.11
-- Date: Tue Jan  4 19:13:27 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity video_mux is
    port (
        sel: in std_logic_vector(1 downto 0);
        A: in std_logic_vector(5 downto 0);
        B: in std_logic_vector(5 downto 0);
        C: in std_logic_vector(5 downto 0);
        output: out std_logic_vector(5 downto 0)
    );
end entity video_mux;


architecture MyHDL of video_mux is



signal A_num: unsigned(5 downto 0);
signal B_num: unsigned(5 downto 0);
signal C_num: unsigned(5 downto 0);
signal output_num: unsigned(5 downto 0);
signal sel_num: unsigned(1 downto 0);

begin

sel_num <= unsigned(sel);
A_num <= unsigned(A);
B_num <= unsigned(B);
C_num <= unsigned(C);
output <= std_logic_vector(output_num);



VIDEO_MUX_BEHAVIOR: process (C_num, A_num, B_num, sel_num) is
begin
    case sel_num is
        when "00" =>
            output_num <= A_num;
        when "01" =>
            output_num <= B_num;
        when others =>
            output_num <= C_num;
    end case;
end process VIDEO_MUX_BEHAVIOR;

end architecture MyHDL;
