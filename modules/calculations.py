#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from gluon import *

input_data = []
other_players_cards = []
lo_count = [2, 3, 4, 5, 6]
high_count = [1, 10]
acceptable_inputs = {"2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", "t", "j", "q", "k", "a"}
set_of_ten_value_cards = {"T", "J", "Q", "K"}

# This method allows you to input the cards in your hand, returning the total value of your hand and the number of aces
# in it, updating the full_deck list with this info. It also resets the hi_lo_count.
def create_new_hand(session):
        #hi_lo_count = 0
        def input_data_translation(x):
            if x.upper() in set_of_ten_value_cards:
                    return 10
            elif x.upper() == "A":

                    return 1
            else:
                return int(x)
        session.held_hand = [input_data_translation(x) for x in session.held_hand]
        for x in session.held_hand:
            session.full_deck.remove(x)
        # for x in input_data:
        #    if x in lo_count:
        #        hi_lo_count += 1
        #    elif x in high_count:
        #        hi_lo_count -= 1

# Simply prints out value of your hand, pretty useless, to be honest, but here for posterity

def current_value_of_hand(session):
    session.box_1 = sum(session.held_hand)

# The cool bit - this is where it calculates the probably that you draw a card that won't bring you over 21. This is
# actually a very basic and bad way to count cards, and next step is bringing in the high/low card counting system.

def calculate_probabilities(session):
    number_of_aces = session.held_hand.count(1)
    number_of_possible_cards_you_could_draw_if_ace_is_eleven = 0
    def calculate_number_of_cards_you_can_draw(distance_to_being_bust):    
        number_of_possible_cards_you_could_draw = 0
        for x in session.full_deck:
            if x < distance_to_being_bust:
                number_of_possible_cards_you_could_draw += 1
        return number_of_possible_cards_you_could_draw
    
    calculated_no_cards_you_can_draw = calculate_number_of_cards_you_can_draw(22 - sum(session.held_hand))
    session.probability_of_not_going_over_21 = (calculated_no_cards_you_can_draw / len(session.full_deck)) * 100

    if number_of_aces > 0 and sum(session.held_hand) + 10 < 22:
        session.are_there_aces = True
        session.sum_if_making_ace_eleven = sum(session.held_hand) + 10
        calculated_no_cards_you_can_draw_if_ace_eleven = calculate_number_of_cards_you_can_draw(22 - session.sum_if_making_ace_eleven)
        session.probability_of_not_going_over_21_if_ace_is_eleven = (
                                                        calculated_no_cards_you_can_draw_if_ace_eleven / len(
                                                            session.full_deck)) * 100
    else: 
        session.are_there_aces = False

#Return sum_if_making_ace_eleven
def remove_other_players_cards_from_deck(hi_lo_count):
    while True:
        other_players_card_input = input("Please input the cards you know other players hold:\n")
        if other_players_card_input != "0":
            if other_players_card_input in acceptable_inputs:
                other_players_cards.append(other_players_card_input)
            else:
                print("That's not an acceptable input!")
        else:
            break

    for x in other_players_cards:
        if x.upper() in set_of_ten_value_cards:
            x = 10
            session.full_deck.remove(10)
        elif x.upper() == "A":
            x = 1
            session.full_deck.remove(1)
        else:
            x = int(x)
            session.full_deck.remove(x)
    for x in other_players_cards:
        if x in lo_count:
            hi_lo_count += 1
        elif x in high_count:
            hi_lo_count -= 1
    return hi_lo_count

def play(session):
    create_new_hand(session)
    current_value_of_hand(session)
    calculate_probabilities(session)

def get_current_deck():
    return full_deck


# The main method, calls upon the methods above. Do I need to explain that?
#def main():

    # while True:
    #     other_cards_availableyn = input("Do you have any cards from your opponents' hands to put in? Y/N\n")
    #     if other_cards_availableyn == "Y" or other_cards_availableyn == "y":
    #         high_low_card_count = remove_other_players_cards_from_deck(high_low_card_count)
    #         break
    #     elif other_cards_availableyn == "N" or other_cards_availableyn == "n":
    #         break
    #     else:
    #         print("Uh. Sorry, we didn't recognise what you just said. Try again?")
    #         continue
