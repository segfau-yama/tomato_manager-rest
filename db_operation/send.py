import time
import Adafruit_TCS34725
import smbus
import numpy as np

start = time.time()
time.sleep(0.5)
all_color = []
all_coef = []
sample_color = [
    [549, 581, 290, 551, 582, 291, 554, 586, 293, 590, 633, 323, 591, 641, 323,
        600, 661, 345, 606, 661, 333, 615, 707, 375, 621, 676, 354, 658, 724, 389],
    [489, 464, 262, 495, 446, 250, 500, 449, 253, 552, 513, 291, 578, 517, 292,
        584, 550, 320, 585, 574, 326, 600, 572, 329, 604, 558, 323, 686, 655, 378],
    [511, 446, 277, 511, 450, 279, 536, 446, 279, 567, 481, 297, 580, 486, 307,
        597, 503, 322, 606, 550, 324, 620, 565, 323, 642, 559, 336, 647, 545, 342],
    [529, 399, 263, 544, 402, 263, 550, 448, 291, 574, 425, 277, 617, 476, 306,
        630, 465, 299, 632, 542, 338, 683, 564, 351, 690, 572, 360, 691, 602, 366],
    [530, 408, 277, 550, 436, 312, 555, 435, 311, 577, 445, 295, 580, 477, 332,
        586, 432, 312, 593, 494, 335, 594, 447, 316, 597, 450, 303, 605, 454, 311],
    [528, 365, 260, 549, 378, 268, 580, 389, 274, 584, 423, 303, 637, 443, 305,
        639, 443, 308, 641, 451, 314, 644, 453, 317, 646, 469, 338, 673, 502, 356],
    [581, 337, 276, 584, 332, 272, 585, 343, 277, 591, 343, 279, 631, 373, 306,
        635, 380, 309, 643, 390, 316, 655, 418, 338, 663, 408, 334, 665, 419, 339],
    [539, 284, 255, 539, 287, 257, 555, 303, 270, 558, 298, 268, 570, 317, 276,
        575, 309, 278, 575, 311, 276, 613, 352, 309, 618, 344, 305, 626, 364, 320]
]

tcs = Adafruit_TCS34725.TCS34725(
    integration_time=Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_154MS)
tcs.set_interrupt(False)
for i in range(10):
    # i2c通信によりred, green, blue, cの値を読む
    red, green, blue, c = tcs.get_raw_data()
    # 色温度の計算
    color_temp = Adafruit_TCS34725.calculate_color_temperature(
        red, green, blue)
    # lx(光度)の計算
    lux = Adafruit_TCS34725.calculate_lux(red, green, blue)
    # red, greenの値を出力
    print('Color:{0} {1}'.format(red, green))
    all_color.append([red, green, blue])
tcs.set_interrupt(True)
tcs.disable()
all_color = np.array(sorted(all_color))
all_color = all_color.flatten()
for i in range(8):
    color_coef = np.corrcoef(sample_color[i], all_color)
    all_coef.append(color_coef[0][1])
print(all_coef)
print("Maturity is {}.".format(all_coef.index(max(all_coef))+1))
elapsed_time = time.time() - start
print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
