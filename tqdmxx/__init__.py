import sys
import time
import locale

class tqdmxx:
    """
    进度条库，提供多种样式的进度条实现
    """

    # 支持的语言
    LANGUAGES = {
        'en': {
            'help_title': '===== tqdmxx Library Help =====',
            'init': '1. Initialize Progress Bar:',
            'params': '2. Optional Parameters:',
            'total': '  - total: Total workload (required)',
            'width': '  - width: Progress bar width (default 50)',
            'style': '  - style: Progress bar style (default \'classic\')',
            'prefix': '  - prefix: Prefix text (default \'Progress:\')',
            'suffix': '  - suffix: Suffix text (default \'%(percent)d%%\')',
            'fill_char': '  - fill_char: Filled character (default \'#\')',
            'empty_char': '  - empty_char: Empty character (default \'-\')',
            'color': '  - color: Color (optional: red, green, yellow, blue, purple, cyan, white)',
            'update_interval': '  - update_interval: Update interval (seconds) (default 0.1)',
            'available_styles': '3. Available Styles:',
            'classic': '  - classic: Classic style',
            'filled': '  - filled: Filled style',
            'dotted': '  - dotted: Dotted style',
            'arrows': '  - arrows: Arrows style',
            'brackets': '  - brackets: Brackets style',
            'boxes': '  - boxes: Boxes style',
            'wave': '  - wave: Wave style',
            'pulse': '  - pulse: Pulse style',
            'spinner': '  - spinner: Spinner style',
            'gradient': '  - gradient: Gradient style',
            'rainbow': '  - rainbow: Rainbow style',
            'bounce': '  - bounce: Bounce style',
            'digital': '  - digital: Digital style',
            'methods': '4. Available Methods:',
            'update': '  - update(increment=1): Update progress',
            'reset': '  - reset(): Reset progress bar',
            'finish': '  - finish(): Force finish progress bar',
            'set_language': '  - set_language(lang): Set display language',
            'get_language': '  - get_language(): Get current language',
            'format_vars': '5. Suffix Format Variables:',
            'percent': '  - %(percent)d%%: Percentage',
            'current': '  - %(current)d: Current progress',
            'total': '  - %(total)d: Total progress',
            'remaining': '  - %(remaining)d: Remaining time',
            'rate': '  - %(rate).2f: Processing rate',
            'example': '6. Usage Example:',
            'current_language': 'Current language: %s'
        },
        'zh': {
            'help_title': '===== tqdmxx 库使用帮助 =====',
            'init': '1. 初始化进度条:',
            'params': '2. 可选参数:',
            'total': '  - total: 总工作量 (必需)',
            'width': '  - width: 进度条宽度 (default50)',
            'style': '  - style: 进度条样式 (default\'classic\')',
            'prefix': '  - prefix: 前缀文本 (default\'Progress:\')',
            'suffix': '  - suffix: 后缀文本 (default\'%(percent)d%%\')',
            'fill_char': '  - fill_char: 已完成部分字符 (default\'#\')',
            'empty_char': '  - empty_char: 未完成部分字符 (default\'-\')',
            'color': '  - color: 颜色 (optional: red, green, yellow, blue, purple, cyan, white)',
            'update_interval': '  - update_interval: 更新间隔(秒) (default0.1)',
            'available_styles': '3. 可用样式:',
            'classic': '  - classic: 经典样式',
            'filled': '  - filled: 填充样式',
            'dotted': '  - dotted: 点状样式',
            'arrows': '  - arrows: 箭头样式',
            'brackets': '  - brackets: 括号样式',
            'boxes': '  - boxes: 方块样式',
            'wave': '  - wave: 波浪样式',
            'pulse': '  - pulse: 脉冲样式',
            'spinner': '  - spinner: 旋转样式',
            'gradient': '  - gradient: 渐变样式',
            'rainbow': '  - rainbow: 彩虹样式',
            'bounce': '  - bounce: 弹跳样式',
            'digital': '  - digital: 数字样式',
            'methods': '4. 可用方法:',
            'update': '  - update(increment=1): 更新进度',
            'reset': '  - reset(): 重置进度条',
            'finish': '  - finish(): 强制完成进度条',
            'set_language': '  - set_language(lang): 设置显示语言',
            'get_language': '  - get_language(): 获取当前语言',
            'format_vars': '5. 后缀格式化变量:',
            'percent': '  - %(percent)d%%: 百分比',
            'current': '  - %(current)d: 当前进度',
            'total': '  - %(total)d: 总进度',
            'remaining': '  - %(remaining)d: 剩余时间',
            'rate': '  - %(rate).2f: 处理速率',
            'example': '6. 使用示例:',
            'current_language': '当前语言: %s'
        }
    }

    # 类变量，存储当前语言设置
    _current_language = 'en'

    def __init__(self, total: int, width: int = 50, style: str = "classic",
                 prefix: str = "Progress:", suffix: str = "%(percent)d%%",
                 fill_char: str = "#", empty_char: str = "-",
                 color: str = None, update_interval: float = 0.1,
                 language: str = None):
        """
        初始化进度条

        参数:
            total: 总工作量
            width: 进度条宽度
            style: 进度条样式，可选值: classic, filled, dotted, arrows, brackets, boxes, wave, pulse, spinner, gradient, rainbow, bounce, digital
            prefix: 进度条前缀文本
            suffix: 进度条后缀文本，支持格式化变量: percent, current, total, remaining, rate
            fill_char: 已完成部分的字符
            empty_char: 未完成部分的字符
            color: 进度条颜色，可选值: red, green, yellow, blue, purple, cyan, white
            update_interval: 进度条更新间隔(秒)
            language: 语言设置，可选值: en, zh
        """
        self.total = total
        self.width = width
        self.style = style
        self.prefix = prefix
        self.suffix = suffix
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.color = color
        self.update_interval = update_interval
        self.current = 0
        self.last_updated = 0
        self.start_time = time.time()
        self.last_output_length = 0  # 记录上次输出的长度

        self._progress_bars = {
            "classic": self._classic_progress,
            "filled": self._filled_progress,
            "dotted": self._dotted_progress,
            "arrows": self._arrows_progress,
            "brackets": self._brackets_progress,
            "boxes": self._boxes_progress,
            "wave": self._wave_progress,
            "pulse": self._pulse_progress,
            "spinner": self._spinner_progress,
            "gradient": self._gradient_progress,
            "rainbow": self._rainbow_progress,
            "bounce": self._bounce_progress,
            "digital": self._digital_progress
        }

        # 设置语言
        if language:
            self.set_language(language)
        else:
            self._current_language = self._detect_system_language()

        if style not in self._progress_bars:
            raise ValueError(f"不支持的进度条样式: {style}")

    def update(self, increment: int = 1) -> None:
        """
        更新进度条

        参数:
            increment: 增加的进度值
        """
        self.current += increment
        current_time = time.time()

        # 控制更新频率
        if current_time - self.last_updated >= self.update_interval or self.current >= self.total:
            self._display()
            self.last_updated = current_time

    def reset(self) -> None:
        """重置进度条"""
        self.current = 0
        self.start_time = time.time()
        self.last_updated = 0
        self.last_output_length = 0
        self._display()

    def finish(self) -> None:
        """强制完成进度条"""
        self.current = self.total
        self._display()
        sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def set_language(lang: str) -> None:
        """设置显示语言"""
        if lang in tqdmxx.LANGUAGES:
            tqdmxx._current_language = lang
        else:
            print(f"不支持的语言: {lang}，使用默认语言")

    @staticmethod
    def get_language() -> str:
        """获取当前语言"""
        return tqdmxx._current_language

    def _display(self) -> None:
        """显示进度条"""
        percent = self.current / self.total if self.total > 0 else 1
        elapsed_time = time.time() - self.start_time
        rate = self.current / elapsed_time if elapsed_time > 0 else 0
        remaining = (self.total - self.current) / rate if rate > 0 else 0

        # 格式化后缀
        formatted_suffix = self.suffix % {
            "percent": int(percent * 100),
            "current": self.current,
            "total": self.total,
            "remaining": remaining,
            "rate": rate
        }

        # 生成进度条
        progress_bar = self._progress_bars[self.style](percent)

        # 添加颜色
        if self.color:
            progress_bar = self._add_color(progress_bar, self.color)

        # 构建完整输出
        output = f"\r{self.prefix} {progress_bar} {formatted_suffix}"

        # 清除之前的行（如果需要）
        if len(output) < self.last_output_length:
            self._clear_line()

        # 输出并刷新
        sys.stdout.write(output)
        sys.stdout.flush()

        # 记录当前输出长度
        self.last_output_length = len(output)

    def _clear_line(self) -> None:
        """清除当前行"""
        sys.stdout.write("\033[2K\r")  # ANSI转义序列：清除整行并将光标移到行首

    def _classic_progress(self, percent: float) -> str:
        """经典样式进度条"""
        filled_length = int(self.width * percent)
        return (self.fill_char * filled_length +
                self.empty_char * (self.width - filled_length))

    def _filled_progress(self, percent: float) -> str:
        """填充样式进度条"""
        filled_length = int(self.width * percent)
        return f"|{self.fill_char * filled_length}{' ' * (self.width - filled_length)}|"

    def _dotted_progress(self, percent: float) -> str:
        """点状样式进度条"""
        filled_length = int(self.width * percent)
        return (f"{self.fill_char * filled_length}"
                f"{self.empty_char * (self.width - filled_length)}")

    def _arrows_progress(self, percent: float) -> str:
        """箭头样式进度条"""
        filled_length = int(self.width * percent)
        if filled_length > 0 and filled_length < self.width:
            return (f"{self.fill_char * (filled_length - 1)}>"
                    f"{self.empty_char * (self.width - filled_length)}")
        return self._classic_progress(percent)

    def _brackets_progress(self, percent: float) -> str:
        """括号样式进度条"""
        filled_length = int(self.width * percent)
        return f"[{self.fill_char * filled_length}{' ' * (self.width - filled_length)}]"

    def _boxes_progress(self, percent: float) -> str:
        """方块样式进度条"""
        filled_length = int(self.width * percent)
        return (f"█" * filled_length +
                f"░" * (self.width - filled_length))

    def _wave_progress(self, percent: float) -> str:
        """波浪样式进度条"""
        filled_length = int(self.width * percent)
        wave_char = '~'
        return (f"{self.fill_char * (filled_length - 1)}{wave_char}"
                f"{self.empty_char * (self.width - filled_length)}") if filled_length > 0 else self.empty_char * self.width

    def _pulse_progress(self, percent: float) -> str:
        """脉冲样式进度条"""
        filled_length = int(self.width * percent)
        pulse_char = '*'
        pulse_pos = int(time.time() * 3) % self.width
        progress = list(self.fill_char * filled_length + self.empty_char * (self.width - filled_length))
        if 0 <= pulse_pos < self.width:
            progress[pulse_pos] = pulse_char
        return ''.join(progress)

    def _spinner_progress(self, percent: float) -> str:
        """旋转样式进度条"""
        filled_length = int(self.width * percent)
        spinner_chars = ['-', '\\', '|', '/']
        spinner_pos = int(time.time() * 4) % 4
        return (f"{self.fill_char * filled_length}{spinner_chars[spinner_pos]}"
                f"{self.empty_char * (self.width - filled_length - 1)}") if filled_length < self.width else self.fill_char * self.width

    def _gradient_progress(self, percent: float) -> str:
        """渐变样式进度条"""
        filled_length = int(self.width * percent)
        gradient_chars = ['░', '▒', '▓', '█']
        gradient_count = len(gradient_chars)
        gradient_segment = self.width // gradient_count

        progress = []
        for i in range(self.width):
            if i < filled_length:
                segment = min(i // gradient_segment, gradient_count - 1)
                progress.append(gradient_chars[segment])
            else:
                progress.append(self.empty_char)

        return ''.join(progress)

    def _rainbow_progress(self, percent: float) -> str:
        """彩虹样式进度条"""
        filled_length = int(self.width * percent)
        colors = ["\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[94m", "\033[95m"]
        reset = "\033[0m"

        progress = []
        for i in range(self.width):
            if i < filled_length:
                color_idx = int(i * len(colors) / filled_length) % len(colors)
                progress.append(f"{colors[color_idx]}{self.fill_char}{reset}")
            else:
                progress.append(self.empty_char)

        return ''.join(progress)

    def _bounce_progress(self, percent: float) -> str:
        """弹跳样式进度条"""
        filled_length = int(self.width * percent)
        progress = list(self.fill_char * filled_length + self.empty_char * (self.width - filled_length))

        # 弹跳球效果
        ball_pos = int((time.time() * 3) % (self.width * 2))
        if ball_pos < self.width:
            pos = ball_pos
        else:
            pos = self.width * 2 - ball_pos - 1

        if pos < len(progress):
            progress[pos] = 'O'

        return ''.join(progress)

    def _digital_progress(self, percent: float) -> str:
        """数字样式进度条"""
        filled_length = int(self.width * percent)
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        digit_pos = int(time.time() * 5) % len(digits)

        progress = []
        for i in range(self.width):
            if i < filled_length:
                progress.append(digits[(i + digit_pos) % len(digits)])
            else:
                progress.append(self.empty_char)

        return ''.join(progress)

    def _add_color(self, text: str, color: str) -> str:
        """为文本添加颜色"""
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "purple": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "reset": "\033[0m"
        }

        if color in colors:
            return f"{colors[color]}{text}{colors['reset']}"
        return text

    @staticmethod
    def _detect_system_language() -> str:
        """检测系统语言"""
        try:
            lang, _ = locale.getdefaultlocale()
            if lang.startswith('zh'):
                return 'zh'
            return 'en'
        except:
            return 'en'

    @staticmethod
    def help() -> None:
        """显示进度条库的使用帮助"""
        lang = tqdmxx.LANGUAGES.get(tqdmxx._current_language, tqdmxx.LANGUAGES['en'])

        print(f"\n{lang['help_title']}")
        print(f"\n{lang['init']}")
        print(f"   bar = ProgressBar(total=100, style='classic', color='green')")

        print(f"\n{lang['params']}")
        print(f"{lang['total']}")
        print(f"{lang['width']}")
        print(f"{lang['style']}")
        print(f"{lang['prefix']}")
        print(f"{lang['suffix']}")
        print(f"{lang['fill_char']}")
        print(f"{lang['empty_char']}")
        print(f"{lang['color']}")
        print(f"{lang['update_interval']}")

        print(f"\n{lang['available_styles']}")
        print(f"{lang['classic']}")
        print(f"{lang['filled']}")
        print(f"{lang['dotted']}")
        print(f"{lang['arrows']}")
        print(f"{lang['brackets']}")
        print(f"{lang['boxes']}")
        print(f"{lang['wave']}")
        print(f"{lang['pulse']}")
        print(f"{lang['spinner']}")
        print(f"{lang['gradient']}")
        print(f"{lang['rainbow']}")
        print(f"{lang['bounce']}")
        print(f"{lang['digital']}")

        print(f"\n{lang['methods']}")
        print(f"{lang['update']}")
        print(f"{lang['reset']}")
        print(f"{lang['finish']}")
        print(f"{lang['set_language']}")
        print(f"{lang['get_language']}")

        print(f"\n{lang['format_vars']}")
        print(f"{lang['percent']}")
        print(f"{lang['current']}")
        print(f"{lang['total']}")
        print(f"{lang['remaining']}")
        print(f"{lang['rate']}")

        print(f"\n{lang['example']}")
        print("import time")
        print("from tqdmxx import tqdmxx")
        print("bar = tqdmxx(total=100, style='boxes', color='blue')")
        print("for i in range(100):")
        print("   time.sleep(0.05)")
        print("   bar.update()")
        print("bar.finish()\n")

        print(lang['current_language'] % tqdmxx._current_language)


# 示例使用
if __name__ == "__main__":
    # 显示帮助
    tqdmxx.help()

    # 示例1: 经典样式
    print("经典样式进度条:")
    bar = tqdmxx(total=100, style="classic", color="green")
    for i in range(100):
        time.sleep(0.05)
        bar.update()
    bar.finish()

    # 示例2: 方块样式
    print("方块样式进度条:")
    bar = tqdmxx(total=100, style="boxes", color="blue",
                      prefix="Loading:", suffix="%(percent)d%% [%(current)d/%(total)d]")
    for i in range(100):
        time.sleep(0.05)
        bar.update()
    bar.finish()

    # 示例3: 彩虹样式
    print("彩虹样式进度条:")
    bar = tqdmxx(total=100, style="rainbow")
    for i in range(100):
        time.sleep(0.05)
        bar.update()
    bar.finish()

    # 示例4: 弹跳样式
    print("弹跳样式进度条:")
    bar = tqdmxx(total=100, style="bounce", color="purple",
                      prefix="Bounce:")
    for i in range(100):
        time.sleep(0.05)
        bar.update()
    bar.finish()

    # 示例5: 数字样式
    print("数字样式进度条:")
    bar = tqdmxx(total=100, style="digital", color="cyan",
                      prefix="Digital:")
    for i in range(100):
        time.sleep(0.05)
        bar.update()
    bar.finish()

    # 语言切换示例
    print("\n中文帮助:")
    tqdmxx.set_language('zh')
    tqdmxx.help()

    print("\nEnglish Help:")
    tqdmxx.set_language('en')
    tqdmxx.help()