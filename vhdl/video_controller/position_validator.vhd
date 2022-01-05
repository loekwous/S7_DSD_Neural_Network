-- File: ../vhdl/video_controller/position_validator.vhd
-- Generated by MyHDL 0.11
-- Date: Tue Jan  4 17:30:45 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity position_validator is
    port (
        x_pos: in std_logic_vector(6 downto 0);
        sq: out std_logic;
        sine: out std_logic;
        tri: out std_logic
    );
end entity position_validator;


architecture MyHDL of position_validator is



signal x_pos_num: unsigned(6 downto 0);

begin

x_pos_num <= unsigned(x_pos);



POSITION_VALIDATOR_BEHAVIOR: process (x_pos_num) is
begin
    if (x_pos_num < 80) then
        if ((x_pos_num >= 0) and (x_pos_num <= 25)) then
            sq <= '1';
        else
            sq <= '0';
        end if;
        if ((x_pos_num >= 26) and (x_pos_num <= 52)) then
            tri <= '1';
        else
            tri <= '0';
        end if;
        if ((x_pos_num >= 53) and (x_pos_num <= 79)) then
            sine <= '1';
        else
            sine <= '0';
        end if;
    else
        sq <= '0';
        sine <= '0';
        tri <= '0';
    end if;
end process POSITION_VALIDATOR_BEHAVIOR;

end architecture MyHDL;
