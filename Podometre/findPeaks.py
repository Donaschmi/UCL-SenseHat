from math import inf

"""
Function that finds the peaks in a sequence of numbers stored in an array
 Use for step detection, you should apply a simple filter to remove low(uncorrect) peaks as done at the end of the file

"""
def findpeaks(data_array):
	position = 0 # not use but culd be usefull
	previous = data_array[0]
	direction = "up"
	peaks = []
	for element in data_array:
		print(element)
		if element > previous: # data is ascending
			if direction == "down": # but was descending
				peaks.append(element)
				direction = "up"
			else:
				pass
		elif element < previous: # data is descending
			if direction == "up": # but was ascending
				peaks.append(element)
				direction = "down"
			else:
				pass
		position += 1
		previous = element
	print(peaks)
	return peaks

"""
 Real data of a person who walked +-23 steps
 	Raspberry was half in side pocket with USB/ethernet ports Upward
 	572 values for 10 seconds of data. Each point is a magnitude value (sqrt(x^2+y^2+z^2)) where x,y,z are accelerometer data
"""
data = [1.05105,   1.15258,   1.27492,   1.32592,   1.19502,   1.17877,   1.17444,   1.14278,   1.20759,   1.15701,   1.07025,   1.09375,   1.10524,   1.16078,   1.18692,   1.10534,   0.95213,   0.79535,   0.75159,   0.72520,   0.74545,   0.76634,   0.80975,   0.79791,   0.79214,   0.74420,   0.76516,   0.80824,   0.85965,   0.96993,   1.10189,   1.16766,   1.38682,   1.53524,   1.43632,   1.01881,   0.75140,   1.41029,   1.51546,   0.90343,   0.79176,   1.34467,   1.19295,   0.87333,   0.76295,   0.82182,   0.91896,   1.03416,   0.95052,   0.91859,   0.90293,   0.89567,   0.86112,   0.90588,   0.93211,   0.93170,   0.94396,   0.96257,   0.96029,   0.91972,   0.91705,   0.95233,   0.98514,   1.03921,   1.12551,   1.17494,   1.13472,   1.12590,   1.09326,   1.12485,   1.16137,   1.46708,   1.31985,   1.24064,   1.18402,   1.16590,   1.17017,   1.09631,   0.97443,   0.86459,   0.96639,   1.16450,   1.22730,   1.14153,   1.05029,   0.97099,   0.90854,   0.85092,   0.87146,   0.88269,   0.85269,   0.84094,   0.83374,   0.83961,   0.86316,   0.83120,   0.81772,   0.84037,   0.84948,   0.97336,   1.02067,   1.06887,   1.11600,   1.16809,   1.24727,   1.21034,   1.15040,   0.91725,   1.52034,   1.67152,   1.18653,   0.90526,   1.05432,   0.89257,   0.78184,   0.77291,   0.90048,   1.11551,   1.08780,   0.89274,   0.82857,   0.88703,   0.86859,   0.84514,   0.89170,   0.98299,   1.02344,   1.01125,   0.94438,   0.91435,   0.92754,   0.97325,   1.01992,   0.99821,   0.97837,   1.04483,   1.13239,   1.16530,   1.15257,   1.13500,   1.20520,   1.27421,   1.37226,   1.15624,   1.16720,   1.12228,   1.00530,   0.94694,   1.13437,   1.16224,   1.19973,   1.22976,   1.18480,   1.15246,   0.97024,   0.81348,   0.76128,   0.71772,   0.68483,   0.85312,   0.88490,   0.83077,   0.80197,   0.82550,   0.79051,   0.76375,   0.78597,   0.90040,   0.99840,   1.11241,   1.27387,   1.40392,   1.46471,   1.53223,   1.69427,   1.35746,   0.81984,   0.68215,   0.73418,   0.89833,   0.97755,   1.00412,   1.12685,   1.05435,   0.87867,   0.80225,   0.89105,   0.98441,   0.98661,   0.93169,   0.93471,   0.88408,   0.87439,   0.91190,   0.94909,   0.99536,   0.99540,   0.93872,   0.91545,   0.96210,   1.00682,   1.02676,   1.02697,   1.01961,   1.01046,   1.18050,   1.18623,   1.11177,   1.16769,   1.41914,   1.33839,   1.28609,   1.25981,   1.21248,   1.04796,   1.05086,   1.08035,   1.05020,   1.07740,   1.10103,   1.16417,   1.09614,   1.00269,   0.90559,   0.82408,   0.71126,   0.67621,   0.71537,   0.71116,   0.76659,   0.77292,   0.74753,   0.72604,   0.78271,   0.84276,   0.97749,   1.20124,   1.35352,   1.51732,   1.59587,   1.32746,   1.23506,   1.32553,   1.07763,   0.75176,   0.89491,   1.08966,   1.05294,   1.00910,   0.92320,   0.87099,   0.79929,   0.91350,   1.02410,   1.00914,   0.93890,   0.93433,   0.92492,   0.85071,   0.85017,   0.87530,   0.95103,   1.02561,   1.00185,   0.94047,   0.94745,   0.95962,   0.99623,   1.05451,   1.09910,   1.13212,   1.12199,   1.08125,   1.04156,   1.07154,   1.23726,   1.44098,   1.38694,   1.27494,   1.27184,   1.08276,   0.98076,   1.07046,   1.11460,   1.16782,   1.10684,   1.10685,   1.09110,   1.00197,   0.90249,   0.84164,   0.75505,   0.75272,   0.80690,   0.77529,   0.80539,   0.81298,   0.78069,   0.71387,   0.73178,   0.74636,   0.80751,   1.00262,   1.16349,   1.26923,   1.61534,   1.55312,   1.28830,   1.02564,   1.47610,   1.41556,   0.74811,   0.56648,   0.98350,   1.13812,   1.10898,   1.03754,   0.98490,   0.74307,   0.75780,   0.97977,   1.07288,   1.02670,   0.94607,   0.89285,   0.85877,   0.85225,   0.85943,   0.92340,   0.99452,   0.98080,   0.93236,   0.90969,   0.96338,   1.04580,   1.01106,   1.05337,   1.10868,   1.10322,   1.08435,   1.15211,   1.10898,   1.12500,   1.21045,   1.26275,   1.24744,   1.29620,   1.24137,   1.17068,   0.94175,   1.03313,   1.05496,   1.11884,   1.19645,   1.19476,   1.14902,   1.07877,   0.95214,   0.87736,   0.84476,   0.73030,   0.67270,   0.77667,   0.81134,   0.87038,   0.83518,   0.74324,   0.70719,   0.73256,   0.83859,   0.91706,   1.00176,   1.06999,   1.16392,   1.46814,   1.50319,   1.39497,   1.10614,   1.42086,   1.33573,   1.03810,   0.72136,   0.90648,   1.15468,   1.11229,   1.03685,   0.99904,   0.82181,   0.78023,   0.99729,   1.09503,   1.00371,   0.94550,   0.87241,   0.89811,   0.89354,   0.91858,   0.96880,   1.00519,   1.01689,   0.95286,   0.91535,   0.94945,   0.99429,   1.03380,   1.04367,   1.04543,   1.09023,   1.13636,   1.02068,   0.97094,   1.04516,   1.08793,   1.14385,   1.23949,   1.25449,   1.31930,   1.28618,   1.20829,   1.07046,   0.92260,   0.98964,   1.03072,   1.19678,   1.22568,   1.20483,   1.09387,   0.98596,   0.90391,   0.84328,   0.76975,   0.70294,   0.71831,   0.80742,   0.84651,   0.83002,   0.79751,   0.81399,   0.85705,   0.87998,   0.90800,   0.92422,   0.98957,   1.10497,   1.26587,   1.29203,   1.29946,   1.14220,   1.15787,   1.45444,   1.43334,   0.98646,   0.89306,   0.91643,   0.92310,   0.81105,   0.88730,   1.04762,   0.89859,   0.91223,   1.08474,   0.99091,   0.94068,   0.91177,   0.91873,   0.92108,   0.91793,   0.91042,   0.90072,   0.94067,   0.98614,   0.98960,   0.94327,   0.90701,   0.90086,   0.95914,   1.03687,   1.08224,   1.14406,   1.14161,   1.06506,   1.07670,   1.11739,   1.15342,   1.36993,   1.32090,   1.32882,   1.27644,   1.24457,   1.03465,   0.91427,   0.80508,   0.88590,   1.12139,   1.21749,   1.15952,   1.19240,   1.12695,   1.03551,   0.92859,   0.81399,   0.76949,   0.77249,   0.84333,   0.80504,   0.79064,   0.79892,   0.84633,   0.81136,   0.83565,   0.80375,   0.86075,   0.97968,   1.06678,   1.05340,   1.17318,   1.29716,   1.35638,   1.23545,   1.59653,   1.56993,   1.23488,   1.04804,   0.84377,   0.77164,   0.68819,   0.75552,   0.93334,   0.95684,   0.96873,   1.02466,   0.94912,   0.93319,   0.96057,   0.98084,   0.89091,   0.88470,   0.86232,   0.94878,   1.04231,   1.01767,   0.95878,   0.95218,   0.96410,   0.95053,   0.99588,   1.00757,   1.04333,   1.12678,   1.12275,   1.06617,   1.10596,   1.12119,   1.07189,   1.07012,   1.10667,   1.33768,   1.25478,   1.29438,   1.25278,   1.14488,   1.06540,   1.16586,   1.07075,   1.03101,   1.08428,   1.22782,   1.23292,   1.15111,   1.09659,   0.96433,   0.87845]


""" +- steps on grass straight """
data2 = [1.10995,   1.16453,   1.35753,   1.43199,   1.40010,   1.32818,   1.39357,   1.45474,   1.55249,   1.49611,   1.35888,   1.34418,   1.35403,   1.24761,   1.12892,   0.82532,   0.72185,   0.73924,   0.77898,   0.62033,   0.54872,   0.54064,   0.60157,   0.65142,   0.77511,   0.83161,   0.84305,   0.80952,   0.63961,   0.62444,   0.64959,   0.82482,   0.90707,   1.00544,   0.97624,   1.11681,   1.49037,   1.57954,   1.57903,   1.45450,   1.53151,   2.06291,   1.62841,   0.67406,   0.18323,   0.56551,   1.13184,   1.41748,   1.35095,   1.11071,   0.82470,   0.66510,   0.71243,   0.80595,   0.86240,   0.84753,   0.80934,   0.80827,   0.84750,   0.85684,   0.89762,   0.94158,   0.96128,   0.94196,   0.97743,   1.00774,   1.01083,   1.08221,   1.12511,   1.07685,   1.02252,   1.03938,   1.22627,   1.37562,   1.36745,   1.33467,   1.46236,   1.54120,   1.51583,   1.35204,   1.13241,   1.13615,   1.17100,   0.92111,   0.78642,   0.82485,   0.74017,   0.60414,   0.65179,   0.67377,   0.74380,   0.78215,   0.71971,   0.67335,   0.64483,   0.74844,   0.87417,   0.87739,   0.95341,   1.42974,   1.69096,   1.74694,   1.43097,   2.12603,   2.17171,   0.93577,   0.14897,   0.60147,   1.14507,   1.18984,   1.05088,   0.96709,   0.94133,   0.84603,   0.80731,   0.79113,   0.82865,   0.85677,   0.88179,   0.84030,   0.80085,   0.81829,   0.86021,   0.89201,   0.95846,   1.03935,   1.04785,   0.98637,   0.98540,   1.10116,   1.12640,   1.07033,   1.09447,   1.26640,   1.36631,   1.33941,   1.44009,   1.48372,   1.49345,   1.45755,   1.27762,   1.15782,   1.28756,   1.30793,   1.10779,   0.87367,   0.74085,   0.62159,   0.48982,   0.52331,   0.61887,   0.71015,   0.75554,   0.71939,   0.60853,   0.65204,   0.77193,   0.86931,   0.96863,   1.17930,   1.57023,   1.75191,   1.66766,   1.45797,   2.42760,   1.89448,   0.74958,   0.26467,   1.22217,   1.32821,   1.10497,   0.95896,   0.87913,   0.78532,   0.78947,   0.77123,   0.78266,   0.82050,   0.86441,   0.89537,   0.83520,   0.79899,   0.90149,   0.94855,   0.94554,   0.98655,   1.02041,   1.00030,   1.00904,   1.02105,   1.05522,   1.07456,   1.13908,   1.22897,   1.38363,   1.45850,   1.53297,   1.55133,   1.48801,   1.33571,   1.27113,   1.14027,   1.12675,   1.21926,   1.18037,   0.93209,   0.83967,   0.77440,   0.56584,   0.54795,   0.72663,   0.76467,   0.75850,   0.73319,   0.73018,   0.76248,   0.78863,   0.88963,   0.94069,   1.38316,   1.56895,   1.67685,   1.66343,   1.03361,   0.91710,   2.41595,   1.99328,   0.94869,   0.77238,   1.07233,   0.99652,   0.80584,   0.80419,   0.94333,   1.00841,   1.00620,   0.83609,   0.70130,   0.74430,   0.87426,   0.90023,   0.89720,   0.90042,   0.89354,   0.93544,   0.99946,   1.05086,   1.01346,   1.03779,   1.07962,   1.11315,   1.09323,   1.02052,   1.04840,   1.25942,   1.39328,   1.36353,   1.32581,   1.45754,   1.56328,   1.52521,   1.32500,   1.22602,   1.23110,   1.16781,   0.90337,   0.79479,   0.76756,   0.65720,   0.62723,   0.67093,   0.73969,   0.79078,   0.78112,   0.70185,   0.57782,   0.64949,   0.86006,   0.93002,   0.81539,   0.98819,   1.42350,   1.64302,   1.65569,   1.24253,   1.81064,   2.32965,   1.07087,   0.28588,   0.51785,   0.95764,   1.08180,   1.07751,   1.12608,   1.06306,   0.87440,   0.77092,   0.72609,   0.75929,   0.83829,   0.86641,   0.91882,   0.87717,   0.86231,   0.86814,   0.86723,   0.89262,   0.96570,   1.04822,   1.06520,   1.08634,   1.12406,   1.18727,   1.14910,   1.05986,   1.10456,   1.31435,   1.48872,   1.38909,   1.28997,   1.29002,   1.38185,   1.43166,   1.29001,   1.17315,   1.17651,   1.11158,   0.95562,   0.78135,   0.70982,   0.61565,   0.54843,   0.66341,   0.76236,   0.85536,   0.90351,   0.81851,   0.65381,   0.60216,   0.75338,   0.94299,   1.00562,   1.12927,   1.44908,   1.72611,   1.68319,   1.84167,   2.22987,   1.30018,   0.41504,   0.26602,   1.07920,   1.41062,   1.13665,   0.95714,   0.80808,   0.78048,   0.77684,   0.82964,   0.83664,   0.87969,   0.91684,   0.92735,   0.84864,   0.80339,   0.83285,   0.87147,   0.99507,   1.09668,   1.10111,   1.03229,   1.05412,   1.12936,   1.14301,   1.08817,   1.04877,   1.26259,   1.47205,   1.55432,   1.54165,   1.43700,   1.25092,   1.24820,   1.21924,   1.16398,   1.19715,   1.25742,   1.17890,   0.99192,   0.84701,   0.73884,   0.60155,   0.60106,   0.63062,   0.66829,   0.70536,   0.72140,   0.68998,   0.60942,   0.70689,   0.86379,   0.97166,   0.99505,   1.35006,   1.63741,   1.69514,   1.53340,   1.22776,   2.13904,   1.82859,   0.78700,   0.53094,   1.05184,   1.05758,   0.82704,   0.85328,   0.86227,   0.84552,   0.81362,   0.80974,   0.79420,   0.85712,   0.93557,   0.96703,   0.92856,   0.92861,   0.94455,   0.94384,   0.88863,   0.89804,   0.97049,   1.04159,   1.09398,   1.06028,   1.05034,   1.05974,   1.05945,   1.00437,   1.25663,   1.50172,   1.56210,   1.54256,   1.50506,   1.40317,   1.36124,   1.22409,   1.06269,   1.11269,   1.15964,   0.98499,   0.82084,   0.80535,   0.73055,   0.62732,   0.67303,   0.77977,   0.82764,   0.81611,   0.73639,   0.63812,   0.59055,   0.70927,   0.88605,   0.97454,   0.91751,   1.25364,   1.66814,   1.72327,   1.56337,   0.79244,   0.85565,   2.28370,   2.65572,   1.52362,   0.83918,   0.90837,   0.70678,   0.44980,   0.62775,   1.01649,   1.27328,   1.10859,   0.73102,   0.70398,   0.88597,   0.96353,   0.92740,   0.92531,   0.97375,   0.93768,   0.90232,   0.99990,   1.07702,   1.07303,   1.07699,   1.11462,   1.10582,   1.11805,   0.97019,   1.19452,   1.48590,   1.62268,   1.59899,   1.37433,   1.18798,   1.18187,   1.28287,   1.30143,   1.27243,   1.22167,   1.00961,   0.89547,   0.89828,   0.82302,   0.61418,   0.55929,   0.58085,   0.63955,   0.69512,   0.68809,   0.61768,   0.60880,   0.70807,   0.86479,   0.91074,   0.92120,   1.25782,   1.56427,   1.65506,   1.64576,   2.08478,   2.22061,   1.15978,   0.22249,   0.30220,   0.82727,   1.18305,   1.27974,   1.20072,   1.01157,   0.86530,   0.76879,   0.74652,   0.75129,   0.79865,   0.79518,   0.82518,   0.89801,   0.90569,   0.90939,   0.92704,   0.91756,   0.85686,   0.88616,   0.92652,   0.95026,   1.00907,   1.11053,   1.15271,   1.07909,   1.05572,   1.19521,   1.41154,   1.45578,   1.45386,   1.42174,   1.46764,   1.47453,   1.36117,   1.20267,   1.16990,   1.23826,   1.13114,   0.94031,   0.83000,   0.82989,   0.69498,   0.65437,   0.68442,   0.68241,   0.70850]

"""
Get peaks and filter out incorrect ones (low values)
"""
D = findpeaks(data2)
for e in D:
	if e > 1.5:	
		print(e)

