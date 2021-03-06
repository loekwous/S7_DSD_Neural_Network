-- File: ../vhdl/video_controller/ram_module_conc.vhd
-- Generated by MyHDL 0.11
-- Date: Tue Jan 11 13:52:40 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity ram_module_conc is
    port (
        clk: in std_logic;
        din: in std_logic;
        addrw: in std_logic_vector(12 downto 0);
        addrr: in std_logic_vector(12 downto 0);
        we: in std_logic;
        dout: out std_logic;
        nrst: in std_logic
    );
end entity ram_module_conc;


architecture MyHDL of ram_module_conc is



signal addrw_num: unsigned(12 downto 0);
signal addrr_num: unsigned(12 downto 0);
type t_array_mem is array(0 to 4800-1) of std_logic;
signal mem: t_array_mem;

begin

addrw_num <= unsigned(addrw);
addrr_num <= unsigned(addrr);



-- Write to RAM on positive edge of the clock.
-- This function is secured to not write to unexisting locations
RAM_MODULE_CONC_WRITE_HANDLE: process (clk) is
begin
    if rising_edge(clk) then
        if (we = '1') then
            if (signed(resize(addrw_num, 14)) < 4800) then
                mem(to_integer(addrw_num)) <= din;
            else
                mem((4800 - 1)) <= din;
            end if;
        end if;
    end if;
end process RAM_MODULE_CONC_WRITE_HANDLE;

RAM_MODULE_CONC_READ_HANDLE: process (clk) is
begin
    if falling_edge(clk) then
        dout <= mem(to_integer(addrr_num));
    end if;
end process RAM_MODULE_CONC_READ_HANDLE;

end architecture MyHDL;
