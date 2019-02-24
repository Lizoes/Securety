import random   # 引入随机函数模块
from PIL import Image, ImageDraw, ImageFont, ImageFilter


_letter_cases = "abcdefghjkmnpqrstuvwxy"   # 小写字母，去除容易发生混淆的i,l,o,z
_upper_cases = _letter_cases.upper()       # 大写字母
_numbers = "".join(map(str, range(3, 10)))   # 数字
init_chars = "".join((_letter_cases, _upper_cases, _numbers))

"""
创建一张图片
在图片中写入随机字符串
将图片写入到制定文件
打开读取
"""


def create_calidate_code(size=(120, 30), chars=init_chars, img_type="GIF", mode="RGB",
                         bg_color=(255, 255, 255), fg_color=(0, 0, 255),
                         font_size=18, font_type="Monaco.ttf", length=4, draw_lines=True, n_line=(1, 2), draw_points=True,
                         point_chance=2):  # 字体
    width, height = size
    img = Image.new(mode, size, bg_color)
    draw = ImageDraw.Draw(img)

    def get_chars():
        return random.sample(chars, length)

    def create_lines():      # 绘制干扰线
        line_num = random.randint(*n_line)
        for i in range(line_num):
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():  # 绘制干扰点
        chance = min(100, max(0, int(point_chance)))    # [0,100]
        for v in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100-chance:
                    draw.point((v, h), fill=(0, 0, 0))

    def create_str():
        c_change = get_chars()
        strs_draw = " %s " % " ".join(c_change)  # 每个字符前后以空格分开
        strs_ret = "".join(c_change)
        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs_draw)
        print("验证码：", strs_draw)
        draw.text(((width-font_width)/3, (height-font_height)/3), strs_draw, fg_color, font)
        return strs_ret

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    code_strs = create_str()

    # 图形扭曲参数
    params = [1-float(random.randint(1, 2))/100, 0, 0, 0,
              1-float(random.randint(1, 10))/100,
              float(random.randint(1, 2))/500,
              0.001,
              float(random.randint(1, 2))/500]

    img = img.transform(size, Image.PERSPECTIVE, params)   # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)   # 滤镜，边界架加强

    return img, code_strs


