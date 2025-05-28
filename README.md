# ReferenceSorting
  用来辅助整理参考文献格式的Python脚本。
  如果你的参考文献用的格式和要求的不一样，或者用了奇奇怪怪的编号，可以参考本代码样例。

  本人第一次写行研报告，用了非常个性化且不够规范的参考文献格式，形如：
  """
  正文：
  ...
  世界PC市场稳中向好（jan2d）
  ...
  参考文献：
  ...
  jan25d - Canalys. Global PC shipments grew 3.9% to 256 million in 2024. https://www.canalys.com/newsroom/global-pc-shipments-q4-2024
  ...
  """
  其中，jan是月份，25是年份，d是同年同月文献的顺序编号。这种参考文献格式在正文中被放在中文括号"（）"中标注引用，可以想象是十分惨不忍睹的画面。

  因此，我尝试让Deepseek-R1（豆包）帮我撰写了一系列Python代码，把参考文献转为正确的格式，并在删除多余的参考文献后重新按照引用顺序排序和编号。在运行这些代码之后，文章变成了如下形式：
  """
  正文：
  ...
  世界PC市场稳中向好[1]
  ...
  参考文献：
  ...
  [1] Canalys. Global PC shipments grew 3.9% to 256 million in 2024. https://www.canalys.com/newsroom/global-pc-shipments-q4-2024
  ...
  """
  看起来效果还不错，因此有了本仓库。
