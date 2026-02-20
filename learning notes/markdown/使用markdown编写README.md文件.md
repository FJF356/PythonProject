基于基本 Markdown 语法的进阶功能。

## 概述

原始 Markdown 设计文档中概述的 [基本语法](https://www.markdown.cn/docs/tutorial-basics/basic-syntax) 添加了许多日常所需元素，但对某些人来说还不够。这就是扩展语法发挥作用的地方。

一些个人和组织通过添加表格、代码块、语法高亮、URL 自动链接和脚注等其他元素，自行扩展了基本语法。这些元素可以通过使用基于基本 Markdown 语法的轻量级标记语言或向兼容的 Markdown 处理器添加扩展来启用。

## 可用性

并非所有 Markdown 应用程序都支持扩展语法元素。您需要检查应用程序使用的轻量级标记语言是否支持您想要使用的扩展语法元素。如果不支持，您仍然可以在 Markdown 处理器中启用扩展。

### 轻量级标记语言

有几种轻量级标记语言是 Markdown 的超集。它们包含基本语法，并通过添加表格、代码块、语法高亮、URL 自动链接和脚注等其他元素对其进行扩展。许多最流行的 Markdown 应用程序都使用以下轻量级标记语言之一

- [CommonMark](https://commonmark.org/)
- [GitHub 风味 Markdown (GFM)](https://github.github.com/gfm/)
- [Markdown Extra](https://michelf.ca/projects/php-markdown/extra/)
- [MultiMarkdown](https://fletcherpenney.net/multimarkdown/)
- [R Markdown](https://rmarkdown.rstudio.com/)

### Markdown 处理器

有 [数十个 Markdown 处理器](https://github.com/markdown/markdown.github.com/wiki/Implementations) 可用。其中许多允许您添加启用扩展语法元素的扩展。有关更多信息，请查看处理器的文档。

## 表格

要添加表格，请使用三个或更多连字符 (---) 创建每个列的标题，并使用竖线 (|) 分隔每个列。为了兼容性，您还应该在行的两端添加一个竖线。

```
| Syntax      | Description || ----------- | ----------- || Header      | Title       || Paragraph   | Text        |
```

呈现的输出如下所示

|语法|说明|
|---|---|
|标题|标题|
|段落|文本|

单元格宽度可以变化，如下所示。呈现的输出看起来相同。

|Syntax|Description|
|---|---|
|Header|Title|
|Paragraph|Text|

提示

使用连字符和管道创建表格可能很繁琐。要加快这一过程，请尝试使用 [Markdown 表格生成器](https://www.tablesgenerator.com/markdown_tables) 或 [AnyWayData Markdown 导出](https://anywaydata.com/)。使用图形界面构建表格，然后将生成的 Markdown 格式文本复制到文件中。

### 对齐

可以通过在标题行的连字符左侧、右侧或两侧添加冒号 (:) 将列中的文本左对齐、右对齐或居中对齐。

``` text
| Syntax      | Description | Test Text     || :---        |    :----:   |          ---: || Header      | Title       | Here's this   || Paragraph   | Text        | And more      |
```

呈现的输出如下所示

| 语法  | 说明  | 测试文本 |
| --- | --- | ---- |
| 标题  | 标题  | 这是   |
| 段落  | 文本  | 还有更多 |

### 表格中的文本格式设置

可以设置表格中的文本格式。例如，可以添加 [链接](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#links)、[代码](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#code)（仅限反引号 ``` 中的单词或短语，不包括 [代码块](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#code-blocks)）和 [强调](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#emphasis)。

不能使用标题、引用块、列表、水平线、图像或大多数 HTML 标记。

提示

可以使用 HTML 在表格单元格中创建 [换行符](https://www.markdown.cn/docs/tutorial-extras/hacks#line-breaks-within-table-cells) 和添加 [列表](https://www.markdown.cn/docs/tutorial-extras/hacks#lists-within-table-cells)。

### 转义表格中的管道字符

可以通过使用其 HTML 字符代码 (`&#124;`) 在表格中显示管道 (`|`) 字符。

## 围栏式代码块

基本的 Markdown 语法允许通过将行缩进四个空格或一个制表符来创建 [代码块](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#code-blocks)。如果你觉得不方便，请尝试使用围栏式代码块。根据你的 Markdown 处理器或编辑器，你将在代码块之前和之后的行上使用三个反引号 (```) 或三个波浪号 (~~~)。最棒的是什么？你不必缩进任何行！

````
```{  "firstName": "John",  "lastName": "Smith",  "age": 25}```
````

呈现的输出如下所示

```
{  "firstName": "John",  "lastName": "Smith",  "age": 25}
```

提示

需要在代码块中显示反引号？请参阅 [本部分](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#escaping-backticks) 以了解如何转义它们。

### 语法高亮

许多 Markdown 处理器支持对带围栏的代码块进行语法高亮。此功能允许您为代码所用语言添加颜色高亮。要添加语法高亮，请在带围栏的代码块前在反引号旁边指定一种语言。

````
```json{  "firstName": "John",  "lastName": "Smith",  "age": 25}```
````

呈现的输出如下所示

```
{  "firstName": "John",  "lastName": "Smith",  "age": 25}
```

## 脚注

脚注允许您添加注释和参考，而不会使文档正文杂乱。创建脚注时，您添加脚注参考的位置将出现带链接的上标数字。读者可以单击链接跳转到页面底部的脚注内容。

要创建脚注参考，请在方括号内添加插入符号和标识符 (`[^1]`)。标识符可以是数字或单词，但不能包含空格或制表符。标识符仅将脚注参考与脚注本身关联——在输出中，脚注按顺序编号。

使用方括号内的另一个插入符号和数字以及冒号和文本添加脚注 (`[^1]`: My footnote.)。您不必将脚注放在文档末尾。您可以在列表、块引用和表格等其他元素之外的任何位置放置它们。

```
Here's a simple footnote,[^1] and here's a longer one.[^bignote][^1]: This is the first footnote.[^bignote]: Here's one with multiple paragraphs and code.    Indent paragraphs to include them in the footnote.    `{ my code }`    Add as many paragraphs as you like.
```

呈现的输出如下所示

这是一个简单的脚注[1](https://www.markdown.cn/docs/tutorial-basics/extended-syntax#user-content-fn-1)，这是一个较长的脚注[2](https://www.markdown.cn/docs/tutorial-basics/extended-syntax#user-content-fn-2)。

## 标题 ID

许多 Markdown 处理器支持 [标题](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#headings) 的自定义 ID——一些 Markdown 处理器会自动添加它们。添加自定义 ID 允许您直接链接到标题并使用 CSS 修改它们。要添加自定义标题 ID，请在与标题同行的花括号中括起自定义 ID。

```
### My Great Heading \{#custom-id}
```

HTML 如下所示

```
<h3 id="custom-id">My Great Heading</h3>
```

### 链接到标题 ID

您可以通过创建带有数字符号 (#) 和自定义标题 ID 的 [标准链接](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#links) 来链接到文件中带有自定义 ID 的标题。这些通常称为锚链接。

Markdown HTML 渲染输出 [标题 ID](https://www.markdown.cn/docs/tutorial-basics/extended-syntax#heading-ids) [标题 ID](https://www.markdown.cn/docs/tutorial-basics/extended-syntax#heading-ids) 标题 ID

|Markdown|HTML|呈现的输出|
|---|---|---|
|`[标题 ID](#heading-ids)`|`<a href="#heading-ids">标题 ID</a>`|[标题 ID](https://www.markdown.cn/docs/tutorial-basics/extended-syntax#heading-ids)|

其他网站可以通过将自定义标题 ID 添加到网页的完整 URL 来链接到标题（例如，`[标题 ID](http://markdownguide.cn/extended-syntax#heading-ids)`）。

## 定义列表

一些 Markdown 处理器允许您创建术语及其相应定义的定义列表。要创建定义列表，请在第一行键入术语。在下一行，键入冒号，后跟空格和定义。

```
First Term: This is the definition of the first term.Second Term: This is one definition of the second term.: This is another definition of the second term.
```

HTML 如下所示

```
<dl>  <dt>First Term</dt>  <dd>This is the definition of the first term.</dd>  <dt>Second Term</dt>  <dd>This is one definition of the second term. </dd>  <dd>This is another definition of the second term.</dd></dl>
```

呈现的输出如下所示

第一个术语

: 这是第一个术语的定义。

第二个术语

: 这是第二个术语的一个定义。 : 这是第二个术语的另一个定义。

注意

Docusaurus 不支持列表。

## 删除线

您可以通过在单词中间加一条水平线来删除单词。结果看起来像这样。此功能允许您表示某些单词是错误的，不应包含在文档中。要删除单词，请在单词前后使用两个波浪号 (~~)。

```
~~The world is flat.~~ We now know that the world is round.
```

呈现的输出如下所示

~~世界是平的。~~ 我们现在知道世界是圆的。

## 任务列表

任务列表（也称为检查表和待办事项列表）允许您创建带有复选框的项目列表。在支持任务列表的 Markdown 应用程序中，复选框将显示在内容旁边。要创建任务列表，请在任务列表项目前面添加破折号 `(-)` 和带有空格的方括号 (`[ ]`)。要选择一个复选框，请在方括号之间添加一个 x (`[x]`)。

```
- [x] Write the press release- [ ] Update the website- [ ] Contact the media
```

呈现的输出如下所示

- [x]  Write the press release
- [ ]  Update the website
- [ ]  Contact the media

## 表情符号

向 Markdown 文件添加表情符号有两种方法：将表情符号复制并粘贴到 Markdown 格式的文本中，或键入_表情符号简码_。

### 复制和粘贴表情符号

在大多数情况下，你可以直接从 [Emojipedia](https://emojipedia.org/) 等来源复制一个表情符号，并将其粘贴到文档中。许多 Markdown 应用程序会自动在 Markdown 格式的文本中显示表情符号。从 Markdown 应用程序导出的 HTML 和 PDF 文件应显示表情符号。

提示

如果你正在使用静态站点生成器，请确保你 [将 HTML 页面编码为 UTF-8](https://www.w3.org/International/tutorials/tutorial-char-enc/)。

### 使用表情符号简码

一些 Markdown 应用程序允许你通过键入表情符号简码来插入表情符号。这些简码以冒号开头和结尾，并包含表情符号的名称。

```
Gone camping! :tent: Be back soon.That is so funny! :joy:
```

呈现的输出如下所示

去露营了！⛺ 马上回来。

太搞笑了！😂

注意

你可以使用此 [表情符号简码列表](https://gist.github.com/rxaviers/7360908)，但请记住，表情符号简码因应用程序而异。有关更多信息，请参阅 Markdown 应用程序的文档。

## 高亮

这种情况并不常见，但一些 Markdown 处理器允许你高亮文本。结果看起来像这样。要高亮单词，请在单词前后使用两个等号 (==)。

```
I need to highlight these ==very important words==.
```

呈现的输出如下所示

我需要高亮这些==非常重要的单词==。

或者，如果你的 Markdown 应用程序支持 [HTML](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#html)，你可以使用 mark HTML 标记。

```
I need to highlight these <mark>very important words</mark>.
```

## 下标

这种情况并不常见，但一些 Markdown 处理器允许你使用下标将一个或多个字符置于正常文本行的下方。要创建下标，请在字符前后使用一个波浪号 (~)。

```
H~2~O
```

呈现的输出如下所示

H~~2~~O

提示

在使用之前，请务必在 Markdown 应用程序中进行测试。一些 Markdown 应用程序在单词前后使用一个波浪号，不是用于下标，而是用于 [删除线](https://www.markdown.cn/docs/tutorial-basics/extended-syntax#strikethrough)。

Docusaurus 中单个波浪号就是删除线。

或者，如果你的 Markdown 应用程序支持 [HTML](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#html)，你可以使用 sub HTML 标记。

```
H<sub>2</sub>O
```

H2O

## 上标

这并不常见，但一些 Markdown 处理器允许你使用上标将一个或多个字符放置在正常文本行上方。要创建上标，请在字符前后使用一个插入符号 (^)。

```
X^2^
```

呈现的输出如下所示

X2

或者，如果你的 Markdown 应用程序支持 HTML，你可以使用 sup HTML 标签。

```
X<sup>2</sup>
```

## 自动 URL 链接

许多 Markdown 处理器会自动将 URL 转换为链接。这意味着如果你键入 [http://www.example.com，你的](http://www.example.xn--com,-yo6f668r/) Markdown 处理器会自动将其转换为一个链接，即使你没有 [使用方括号](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#links)。

```
http://www.example.com
```

呈现的输出如下所示

[http://www.example.com](http://www.example.com/)

## 禁用自动 URL 链接

如果你不希望 URL 被自动链接，你可以通过 [使用反引号将 URL 表示为代码](https://www.markdown.cn/docs/tutorial-basics/basic-syntax#code) 来移除链接。

`http://www.example.com`

呈现的输出如下所示

`http://www.example.com`

## Footnotes

1. 这是脚注1的内容。 [↩](https://www.markdown.cn/docs/tutorial-basics/extended-syntax#user-content-fnref-1)
    
2. 这是一个包含多个段落和代码的脚注。
    
    缩进段落以将其包含在脚注中。
    
    `{ my code }`
    
    可以根据需要添加任意多个段落。 [↩](https://www.markdown.cn/docs/tutorial-basics/extended-syntax#user-content-fnref-2)