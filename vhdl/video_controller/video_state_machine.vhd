-- File: ../vhdl/video_controller/video_state_machine.vhd
-- Generated by MyHDL 0.11
-- Date: Sun Jan  9 13:20:01 2022


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_011.all;

entity video_state_machine is
    port (
        timing_pins_clk: in std_logic;
        timing_pins_nrst: in std_logic;
        int_inputs_drawn_outputs_sq_o: in std_logic;
        int_inputs_drawn_outputs_sin_o: in std_logic;
        int_inputs_drawn_outputs_tri_o: in std_logic;
        int_inputs_ch_max: in std_logic;
        int_inputs_val_sq: in std_logic;
        int_inputs_val_tri: in std_logic;
        int_inputs_val_sin: in std_logic;
        int_inputs_x_count_top: in std_logic;
        ext_inputs_triangle: in std_logic;
        ext_inputs_sine: in std_logic;
        ext_inputs_square: in std_logic;
        int_outputs_drawn_inputs_clr: out std_logic;
        int_outputs_drawn_inputs_sq_t: out std_logic;
        int_outputs_drawn_inputs_tri_t: out std_logic;
        int_outputs_drawn_inputs_sin_t: out std_logic;
        int_outputs_sel_output: out std_logic_vector(1 downto 0);
        int_outputs_clr_x: out std_logic;
        int_outputs_clr_sin: out std_logic;
        int_outputs_clr_tri: out std_logic;
        int_outputs_clr_sq: out std_logic;
        int_outputs_ch_en: out std_logic;
        ext_outputs_pixel: out std_logic;
        ext_outputs_we: out std_logic
    );
end entity video_state_machine;


architecture MyHDL of video_state_machine is


type t_enum_t_functs_1 is (
	FNONE,
	FSINE,
	FTRIANGLE,
	FSQUARE
	);
type t_enum_t_states_2 is (
	SINIT,
	IDLE,
	SET_SINE,
	RES_SINE,
	SET_TRIANGLE,
	RES_TRIANGLE,
	SET_SQUARE,
	RES_SQUARE,
	NAME
	);

signal func: t_enum_t_functs_1;
signal n_s: t_enum_t_states_2;
signal p_s: t_enum_t_states_2;
signal int_outputs_sel_output_num: unsigned(1 downto 0);

begin

int_outputs_sel_output <= std_logic_vector(int_outputs_sel_output_num);



VIDEO_STATE_MACHINE_SEL_FUNCTION: process (func) is
begin
    case func is
        when FNONE =>
            int_outputs_clr_sin <= '1';
            int_outputs_clr_sq <= '1';
            int_outputs_clr_tri <= '1';
            int_outputs_sel_output_num <= to_unsigned(0, 2);
            ext_outputs_we <= '0';
        when FSINE =>
            int_outputs_clr_sin <= '0';
            int_outputs_clr_sq <= '1';
            int_outputs_clr_tri <= '1';
            int_outputs_sel_output_num <= to_unsigned(0, 2);
            ext_outputs_we <= '1';
        when FTRIANGLE =>
            int_outputs_clr_sin <= '1';
            int_outputs_clr_sq <= '1';
            int_outputs_clr_tri <= '0';
            int_outputs_sel_output_num <= to_unsigned(1, 2);
            ext_outputs_we <= '1';
        when others =>
            int_outputs_clr_sin <= '1';
            int_outputs_clr_sq <= '0';
            int_outputs_clr_tri <= '1';
            int_outputs_sel_output_num <= to_unsigned(2, 2);
            ext_outputs_we <= '1';
    end case;
end process VIDEO_STATE_MACHINE_SEL_FUNCTION;

VIDEO_STATE_MACHINE_INPUT_DECODER: process (ext_inputs_sine, int_inputs_drawn_outputs_tri_o, ext_inputs_triangle, p_s, int_inputs_x_count_top, int_inputs_ch_max, int_inputs_drawn_outputs_sin_o, int_inputs_drawn_outputs_sq_o, ext_inputs_square) is
begin
    if (p_s = SINIT) then
        n_s <= NAME;
    elsif ((p_s = NAME) and (int_inputs_ch_max = '1')) then
        n_s <= IDLE;
    elsif (p_s = IDLE) then
        if ((ext_inputs_sine = '1') and (int_inputs_drawn_outputs_sin_o = '0')) then
            n_s <= SET_SINE;
        elsif ((ext_inputs_sine = '0') and (int_inputs_drawn_outputs_sin_o = '1')) then
            n_s <= RES_SINE;
        elsif ((ext_inputs_square = '1') and (int_inputs_drawn_outputs_sq_o = '0')) then
            n_s <= SET_SQUARE;
        elsif ((ext_inputs_square = '0') and (int_inputs_drawn_outputs_sq_o = '1')) then
            n_s <= RES_SQUARE;
        elsif ((ext_inputs_triangle = '1') and (int_inputs_drawn_outputs_tri_o = '0')) then
            n_s <= SET_TRIANGLE;
        elsif ((ext_inputs_triangle = '0') and (int_inputs_drawn_outputs_tri_o = '1')) then
            n_s <= RES_TRIANGLE;
        else
            n_s <= IDLE;
        end if;
    elsif (((p_s = SET_SINE) or (p_s = RES_SINE) or (p_s = SET_SQUARE) or (p_s = RES_SQUARE) or (p_s = SET_TRIANGLE) or (p_s = RES_TRIANGLE)) and (int_inputs_x_count_top = '1')) then
        n_s <= IDLE;
    else
        n_s <= p_s;
    end if;
end process VIDEO_STATE_MACHINE_INPUT_DECODER;

VIDEO_STATE_MACHINE_MEM: process (timing_pins_clk, timing_pins_nrst) is
begin
    if (timing_pins_nrst = '0') then
        p_s <= SINIT;
    elsif rising_edge(timing_pins_clk) then
        p_s <= n_s;
    end if;
end process VIDEO_STATE_MACHINE_MEM;

VIDEO_STATE_MACHINE_OUTPUT_DECODER_CHAR: process (p_s) is
begin
    if (p_s = NAME) then
        int_outputs_ch_en <= '1';
    else
        int_outputs_ch_en <= '0';
    end if;
end process VIDEO_STATE_MACHINE_OUTPUT_DECODER_CHAR;

VIDEO_STATE_MACHINE_OUTPUT_DECODER_PIXEL: process (p_s, int_inputs_val_tri, int_inputs_val_sq, int_inputs_val_sin) is
begin
    if (((p_s = SET_SINE) and (int_inputs_val_sin = '1')) or ((p_s = SET_SQUARE) and (int_inputs_val_sq = '1')) or ((p_s = SET_TRIANGLE) and (int_inputs_val_tri = '1'))) then
        ext_outputs_pixel <= '1';
    else
        ext_outputs_pixel <= '0';
    end if;
end process VIDEO_STATE_MACHINE_OUTPUT_DECODER_PIXEL;

VIDEO_STATE_MACHINE_OUTPUT_DECODER_FUNC: process (p_s, int_inputs_val_tri, int_inputs_val_sq, int_inputs_val_sin) is
begin
    if ((p_s = SET_SINE) or (p_s = RES_SINE)) then
        int_outputs_clr_x <= '0';
        if (int_inputs_val_sin = '1') then
            func <= FSINE;
        else
            func <= FNONE;
        end if;
    elsif ((p_s = SET_SQUARE) or (p_s = RES_SQUARE)) then
        int_outputs_clr_x <= '0';
        if (int_inputs_val_sq = '1') then
            func <= FSQUARE;
        else
            func <= FNONE;
        end if;
    elsif ((p_s = SET_TRIANGLE) or (p_s = RES_TRIANGLE)) then
        int_outputs_clr_x <= '0';
        if (int_inputs_val_tri = '1') then
            func <= FTRIANGLE;
        else
            func <= FNONE;
        end if;
    else
        int_outputs_clr_x <= '1';
        func <= FNONE;
    end if;
end process VIDEO_STATE_MACHINE_OUTPUT_DECODER_FUNC;

VIDEO_STATE_MACHINE_OUTPUT_DECODER_MEM: process (ext_inputs_sine, int_inputs_drawn_outputs_tri_o, ext_inputs_triangle, p_s, int_inputs_drawn_outputs_sin_o, int_inputs_drawn_outputs_sq_o, ext_inputs_square) is
begin
    case p_s is
        when SINIT =>
            int_outputs_drawn_inputs_clr <= '1';
            int_outputs_drawn_inputs_sin_t <= '0';
            int_outputs_drawn_inputs_sq_t <= '0';
            int_outputs_drawn_inputs_tri_t <= '0';
        when IDLE =>
            int_outputs_drawn_inputs_clr <= '0';
            if (int_inputs_drawn_outputs_sin_o /= ext_inputs_sine) then
                int_outputs_drawn_inputs_sin_t <= '1';
            else
                int_outputs_drawn_inputs_sin_t <= '0';
            end if;
            if (int_inputs_drawn_outputs_sq_o /= ext_inputs_square) then
                int_outputs_drawn_inputs_sq_t <= '1';
            else
                int_outputs_drawn_inputs_sq_t <= '0';
            end if;
            if (int_inputs_drawn_outputs_tri_o /= ext_inputs_triangle) then
                int_outputs_drawn_inputs_tri_t <= '1';
            else
                int_outputs_drawn_inputs_tri_t <= '0';
            end if;
        when others =>
            int_outputs_drawn_inputs_clr <= '0';
            int_outputs_drawn_inputs_sin_t <= '0';
            int_outputs_drawn_inputs_sq_t <= '0';
            int_outputs_drawn_inputs_tri_t <= '0';
    end case;
end process VIDEO_STATE_MACHINE_OUTPUT_DECODER_MEM;

end architecture MyHDL;
