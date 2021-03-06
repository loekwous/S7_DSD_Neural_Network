-- File: vhdl_out/codec_controller.vhd
-- Generated by MyHDL 0.11
-- Date: Tue Jan 25 21:06:43 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity codec_controller is
    port (
        clk: in std_logic;
        nrst: in std_logic;
        start: in std_logic;
        ready: out std_logic;
        i2c_start: out std_logic;
        i2c_ready: in std_logic;
        i2c_success: in std_logic;
        cnt_clr: out std_logic;
        cnt_up: out std_logic;
        cnt_top: in std_logic
    );
end entity codec_controller;


architecture MyHDL of codec_controller is


type t_enum_t_states_1 is (
	IDLE,
	WF_START,
	START_SENDING,
	WAIT_FOR_TRANS,
	COUNT_UP
	);

signal n_s: t_enum_t_states_1;
signal p_s: t_enum_t_states_1;

begin




CODEC_CONTROLLER_INPUT_DECODER: process (start, i2c_success, i2c_ready, cnt_top, p_s) is
begin
    if ((p_s = IDLE) and (start = '1')) then
        n_s <= WF_START;
    elsif ((p_s = WF_START) and (start = '0')) then
        n_s <= START_SENDING;
    elsif ((p_s = START_SENDING) and (i2c_ready = '0')) then
        n_s <= WAIT_FOR_TRANS;
    elsif (p_s = WAIT_FOR_TRANS) then
        if (i2c_ready = '1') then
            if (i2c_success = '1') then
                if (cnt_top = '1') then
                    n_s <= IDLE;
                else
                    n_s <= COUNT_UP;
                end if;
            else
                n_s <= IDLE;
            end if;
        else
            n_s <= WAIT_FOR_TRANS;
        end if;
    elsif (p_s = COUNT_UP) then
        n_s <= START_SENDING;
    else
        n_s <= p_s;
    end if;
end process CODEC_CONTROLLER_INPUT_DECODER;

CODEC_CONTROLLER_MEMORY: process (clk, nrst) is
begin
    if (nrst = '0') then
        p_s <= IDLE;
    elsif rising_edge(clk) then
        p_s <= n_s;
    end if;
end process CODEC_CONTROLLER_MEMORY;


i2c_start <= tern_op(cond => (p_s = START_SENDING), if_true => '1', if_false => '0');

CODEC_CONTROLLER_CLEAR_CONTROL: process (p_s) is
    variable clear_condition: std_logic;
begin
    clear_condition := stdl((p_s = IDLE) or (p_s = WF_START));
    cnt_clr <= tern_op(cond => bool(clear_condition), if_true => '1', if_false => '0');
end process CODEC_CONTROLLER_CLEAR_CONTROL;


cnt_up <= tern_op(cond => (p_s = COUNT_UP), if_true => '1', if_false => '0');


ready <= tern_op(cond => (p_s = IDLE), if_true => '1', if_false => '0');

end architecture MyHDL;
