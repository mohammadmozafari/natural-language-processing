import unittest
from main import *

TEST_FOLDER = 'test_case'

class test_program(unittest.TestCase):
	def test_extract(self):
		self.assertListEqual(extract_phrases('123  ۴5۶'), ['123', '۴5۶'])
		self.assertListEqual(extract_phrases('من و صد و بیست و سه نفر دیگر'), ['صد و بیست و سه'])
		self.assertListEqual(extract_phrases('۲ میلیون و ۳ هزار و چهار اسب بارکش به همراه نوزده نفر سرباز'), ['۲ میلیون و ۳ هزار و چهار', 'نوزده'])

	def test_get_value_digit(self):
		self.assertEqual(get_value_digit('123')[0], 123)
		self.assertEqual(get_value_digit('1۲3')[0], 123)
		self.assertEqual(get_value_digit('۷۰۸1۲')[0], 70812)
		self.assertEqual(get_value_digit('۱۲۰')[0], 120)

	def test_get_value(self):
		self.assertEqual(get_value('صد و بیست و سه'), 123)
		self.assertEqual(get_value('۲ میلیون و ۳ هزار و چهار'), 2003004)
		self.assertEqual(get_value('بیست هزار میلیارد و ۱۱۵ میلیون'), 20 * 10**12 + 115*10**6)
		self.assertEqual(get_value('صفر'), 0)
		self.assertEqual(get_value('منفی سه'), -3)
		self.assertEqual(get_value('-123'), -123)
		self.assertEqual(get_value('منفی دو هزار و پانصد و ۳ میلیون'), -2503 * 10**6)
		self.assertEqual(get_value('پانصد و بیست و سه هزار و ۱۰۰ و ۲۴'), 523124)

		self.assertEqual(45.6, get_value('چهل و 5 و شش دهم'))
		self.assertEqual(12000.5, get_value('دوازده هزار و نیم'))
		self.assertEqual(510000.5, get_value('نیم میلیون و 10 هزار و 5 دهم'))

	def test_number_extractor(self):
		self.assertListEqual(number_extractor('123  ۴5۶'),
			[
				{
					'phrase': '123',
					'value': 123
			 	},
				{
					'phrase': '۴5۶',
					'value': 456
				}
			]
		 )
		self.assertListEqual(number_extractor('بیست هزار میلیارد و ۱۱۵ میلیون و هفتصد و نود و نه هزار و پانصد و بیست و ۳ اسب وحشی در سال ۲ هزار و چهارده میلادی با صد و ۱۰ قاطر معاوضه گردیدند.'),
			[
				{
					'phrase': 'بیست هزار میلیارد و ۱۱۵ میلیون و هفتصد و نود و نه هزار و پانصد و بیست و ۳',
					'value': 20000115799523
			 	},
				{
					'phrase': '۲ هزار و چهارده',
					'value': 2014
				},
				{
					'phrase': 'صد و ۱۰',
					'value': 110
				}
			]
		 )
		self.assertListEqual(number_extractor('صد و۱ و ۲و۳ و ۴و ۶'),
			[
				{
					'phrase': 'صد و۱',
					'value': 101
			 	},
				{
					'phrase': '۲',
					'value': 2
				},
				{
					'phrase': '۳',
					'value': 3
				},
				{
					'phrase': '۴',
					'value': 4
				},
				{
					'phrase': '۶',
					'value': 6
				},
			]
		 )
		self.assertListEqual(number_extractor('صد و۱ و پنجاه و سه'),
			[
				{
					'phrase': 'صد و۱',
					'value': 101
			 	},
				{
					'phrase': 'پنجاه و سه',
					'value': 53
				}
			]
		 )

	def test_folder(self):
		for i in range(1, 21):
			with open(f'{TEST_FOLDER}/in/input{i}.txt', 'r', encoding='utf-8') as f_input:
				with open(f'{TEST_FOLDER}/out/output{i}.txt', 'r', encoding='utf-8') as f_output:
					input_data = f_input.read()
					actual = [item['value'] for item in number_extractor(input_data)]
					output_data = f_output.read()
					expected = [float(line) for line in output_data.rstrip().split('\n')]
					try:
						self.assertListEqual(expected, actual)
					except Exception as ex:
						print(i)
						print(str(ex).split('\n')[0])

if __name__ == '__main__':
	unittest.main()