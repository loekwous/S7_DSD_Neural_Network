-- File: ../vhdl/video_controller/mod_counter.vhd
-- Generated by MyHDL 0.11
-- Date: Sun Jan  9 13:20:01 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity mod_counter is
    port (
        clk: in std_logic;
        en: in std_logic;
        clr: in std_logic;
        dout: out std_logic_vector(6 downto 0);
        top: out std_logic
    );
end entity mod_counter;


architecture MyHDL of mod_counter is



signal counter: unsigned(6 downto 0);
signal dout_num: unsigned(6 downto 0);

begin

dout <= std_logic_vector(dout_num);




dout_num <= counter;

MOD_COUNTER_UPDATE_TOP: process (counter) is
begin
    if (signed(resize(counter, 8)) = (81 - 2)) then
        top <= '1';
    else
        top <= '0';
    end if;
end process MOD_COUNTER_UPDATE_TOP;

MOD_COUNTER_UPDATE_COUNTER: process (clk) is
begin
    if rising_edge(clk) then
        if (clr = '1') then
            counter <= to_unsigned(0, 7);
        else
            if (clr = '1') then
                counter <= to_unsigned(0, 7);
            elsif (en = '1') then
                if (signed(resize(counter, 8)) < (81 - 2)) then
                    counter <= (counter + 1);
                else
                    counter <= to_unsigned(0, 7);
                end if;
            end if;
        end if;
    end if;
end process MOD_COUNTER_UPDATE_COUNTER;

end architecture MyHDL;
