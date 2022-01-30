import typing
import math
import re
from pattern import *

def extract_phrases(input_sentence: str) -> typing.List[str]:
	input_sentence = re.sub(f'({PATTERN_NUMBER_WITH_DIGITS})', r' \1 ', input_sentence)  # adding space around digits
	phrases = re.findall(PATTERN_SEARCH, input_sentence)
	for index, phrase in enumerate(phrases):
		phrases[index] = re.sub(f' ?({PATTERN_NUMBER_WITH_DIGITS}) ?', r'\1', phrase)   # reverting space around digits
	return phrases

def get_value_digit(sub_phrase: str) -> typing.Tuple[float]:
	intab = PERSIAN_ZERO_DIGIT + PERSIAN_NON_ZERO_DIGITS + '٫'
	outtab = ENGLISH_ZERO_DIGIT + ENGLISH_NON_ZERO_DIGITS + '.'
	translation = str.maketrans(intab, outtab)
	return float(sub_phrase.translate(translation)),

def get_value_simple(sub_phrase: str) -> typing.Tuple[float]:
	return ALL_PERSIAN_SIMPLE_NUMBERS[sub_phrase],

def get_value_extend(sub_phrase: str) -> tuple:
	multiplier = 1

	before_extend = re.findall(PATTERN_BEFORE_EXTEND, sub_phrase)[0]
	before_extend_value = get_value(before_extend)  # a digit_Value or a simple value
	sub_phrase = re.sub(PATTERN_BEFORE_EXTEND, '', sub_phrase, 1)  # remove before extend part

	extends = re.findall(PATTERN_EXTEND, sub_phrase)

	for extend in extends:
		multiplier *= PERSIAN_REQUIRED_EXTENDABLE_NUMBERS[extend]

	if multiplier < 1:
		return before_extend_value * multiplier,

	return before_extend_value, multiplier

def get_sub_phrase_value(sub_phrase: str) -> tuple:
	get_value_mapper = {
		'EXTENDED': get_value_extend,
		'DIGIT': get_value_digit,
		'SIMPLE': get_value_simple
	}
	for sub_phrase_kind, sub_phrase_pattern in ALL_PARTS.items():
		if re.match(sub_phrase_pattern, sub_phrase):
			return get_value_mapper[sub_phrase_kind](sub_phrase)

def get_value(phrase: str) -> float:
	return_value = 0
	temp_value = 0
	highest_extend_multiplier = 0
	negative_number = False

	if phrase == PERSIAN_ZERO:
		return 0  # this is zero obviously
	if len(re.findall(ALL_NEGS, phrase)):
		negative_number = True

	sub_phrases = re.findall(PATTERN_SINGLE_NUMBER, phrase)
	sub_phrase_values = map(get_sub_phrase_value, sub_phrases)

	for index, value in enumerate(sub_phrase_values):
		addition = value[0]

		if temp_value != 0:
			if temp_value % 10**math.ceil(math.log(addition, 10)) >= 1:
				raise ValueError(index)  # Panic: There are more than one valid number in the phrase

		temp_value += addition

		if len(value) == 2:
			multiplier = value[1]
			if highest_extend_multiplier < multiplier:
				highest_extend_multiplier = multiplier
				temp_value += return_value
				return_value = 0
			return_value = return_value + temp_value * multiplier
			temp_value = 0

	return_value += temp_value

	if negative_number:
		return_value = -return_value

	return return_value

def number_extractor(input_sentence):
	return_value = []
	phrases = extract_phrases(input_sentence)
	i = 0
	while i < len(phrases):
		try:
			return_value.append({
				'phrase': phrases[i],
				'value': get_value(phrases[i])
			})
			i += 1
		except ValueError as exp:  # Handling line 68 panic
			last_phrase_parts = phrases[i].split(PERSIAN_V, exp.args[0])
			phrase1_end = len(phrases[i]) - len(last_phrase_parts[-1])
			sub_phrase1 = extract_phrases(phrases[i][:phrase1_end])[0]
			sub_phrase2 = extract_phrases(last_phrase_parts[-1])[0]
			phrases[i] = sub_phrase1
			phrases.insert(i + 1, sub_phrase2)
	return return_value
