-- File: vhdl_out/top_level_i2s.vhd
-- Generated by MyHDL 0.11
-- Date: Wed Jan 26 15:17:35 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity top_level_i2s is
    port (
        clk: in std_logic;
        nrst: in std_logic;
        i2s_clk: in std_logic;
        i2s_data: in std_logic;
        i2s_frame: in std_logic;
        dout: out std_logic_vector(23 downto 0);
        rdy: out std_logic
    );
end entity top_level_i2s;


architecture MyHDL of top_level_i2s is


type t_enum_t_states_1 is (
	IDLE,
	DELAY,
	DELAY2,
	CAPTURE,
	WF_LOW,
	WF_HIGH,
	WF_END
	);

signal dout_num: unsigned(23 downto 0);
signal cnt_up: std_logic;
signal cnt_clr: std_logic;
signal cnt_top: std_logic;
signal sipo_en: std_logic;
signal i2s_counter1_counter: unsigned(4 downto 0);
signal i2s_sipo1_sr: unsigned(23 downto 0);
signal i2s_controller1_n_s: t_enum_t_states_1;
signal i2s_controller1_p_s: t_enum_t_states_1;

begin

dout <= std_logic_vector(dout_num);



TOP_LEVEL_I2S_I2S_COUNTER1_OUTPUT_LOGIC: process (i2s_counter1_counter) is
begin
    if (i2s_counter1_counter = 24) then
        cnt_top <= '1';
    else
        cnt_top <= '0';
    end if;
end process TOP_LEVEL_I2S_I2S_COUNTER1_OUTPUT_LOGIC;

TOP_LEVEL_I2S_I2S_COUNTER1_COUNT_LOGIC: process (clk) is
begin
    if rising_edge(clk) then
        if (cnt_clr = '1') then
            i2s_counter1_counter <= to_unsigned(0, 5);
        else
            if (cnt_up = '1') then
                if (i2s_counter1_counter < 24) then
                    i2s_counter1_counter <= (i2s_counter1_counter + 1);
                end if;
            end if;
        end if;
    end if;
end process TOP_LEVEL_I2S_I2S_COUNTER1_COUNT_LOGIC;


dout_num <= i2s_sipo1_sr;

TOP_LEVEL_I2S_I2S_SIPO1_SHIFT_LOGIC: process (clk, nrst) is
begin
    if (nrst = '0') then
        i2s_sipo1_sr <= to_unsigned(0, 24);
    elsif rising_edge(clk) then
        if (sipo_en = '1') then
            i2s_sipo1_sr <= resize(unsigned'(i2s_sipo1_sr((24 - 2)-1 downto 0) & i2s_data), 24);
        end if;
    end if;
end process TOP_LEVEL_I2S_I2S_SIPO1_SHIFT_LOGIC;

TOP_LEVEL_I2S_I2S_CONTROLLER1_INPUT_DECODER: process (i2s_clk, i2s_controller1_p_s, cnt_top, i2s_frame) is
begin
    if ((i2s_controller1_p_s = IDLE) and (i2s_frame = '1') and (i2s_clk = '1')) then
        i2s_controller1_n_s <= DELAY;
    elsif ((i2s_controller1_p_s = DELAY) and (i2s_frame = '1') and (i2s_clk = '0')) then
        i2s_controller1_n_s <= DELAY2;
    elsif ((i2s_controller1_p_s = DELAY2) and (i2s_frame = '1') and (i2s_clk = '1')) then
        i2s_controller1_n_s <= CAPTURE;
    elsif (i2s_controller1_p_s = CAPTURE) then
        i2s_controller1_n_s <= WF_LOW;
    elsif ((i2s_controller1_p_s = WF_LOW) and (i2s_frame = '1') and (i2s_clk = '0')) then
        i2s_controller1_n_s <= WF_HIGH;
    elsif ((i2s_controller1_p_s = WF_HIGH) and (i2s_frame = '1') and (i2s_clk = '1')) then
        if (cnt_top = '1') then
            i2s_controller1_n_s <= WF_END;
        else
            i2s_controller1_n_s <= CAPTURE;
        end if;
    elsif ((i2s_controller1_p_s = WF_END) and (i2s_frame = '0')) then
        i2s_controller1_n_s <= IDLE;
    else
        i2s_controller1_n_s <= i2s_controller1_p_s;
    end if;
end process TOP_LEVEL_I2S_I2S_CONTROLLER1_INPUT_DECODER;

TOP_LEVEL_I2S_I2S_CONTROLLER1_MEMORY: process (clk, nrst) is
begin
    if (nrst = '0') then
        i2s_controller1_p_s <= IDLE;
    elsif rising_edge(clk) then
        i2s_controller1_p_s <= i2s_controller1_n_s;
    end if;
end process TOP_LEVEL_I2S_I2S_CONTROLLER1_MEMORY;

TOP_LEVEL_I2S_I2S_CONTROLLER1_OUTPUT_DECODER: process (i2s_controller1_p_s) is
begin
    case i2s_controller1_p_s is
        when IDLE =>
            sipo_en <= '0';
            cnt_clr <= '1';
            cnt_up <= '0';
            rdy <= '1';
        when DELAY =>
            sipo_en <= '0';
            cnt_clr <= '0';
            cnt_up <= '0';
            rdy <= '0';
        when DELAY2 =>
            sipo_en <= '0';
            cnt_clr <= '0';
            cnt_up <= '0';
            rdy <= '0';
        when CAPTURE =>
            sipo_en <= '1';
            cnt_clr <= '0';
            cnt_up <= '1';
            rdy <= '0';
        when others =>
            sipo_en <= '0';
            cnt_clr <= '0';
            cnt_up <= '0';
            rdy <= '0';
    end case;
end process TOP_LEVEL_I2S_I2S_CONTROLLER1_OUTPUT_DECODER;

end architecture MyHDL;
