# LaTeX Preamble

Publication layout and Unicode-capable source-code typography. TeX resolves
font filenames through its own search path; no machine-specific path is required.

```latex
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{geometry}
\geometry{margin=20mm}
\usepackage{float}
\usepackage{graphicx}
\usepackage{etoolbox}
\AtBeginEnvironment{titlepage}{%
  \renewcommand{\Huge}{\fontsize{22}{26}\selectfont}%
  \renewcommand{\Large}{\fontsize{11}{13}\selectfont}%
  \renewcommand{\large}{\fontsize{11}{13}\selectfont}%
  \renewcommand{\small}{\fontsize{8}{9}\selectfont}%
}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{listings}
\lstset{basicstyle=\ttfamily\small,breaklines=true,columns=fullflexible}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{remark}[theorem]{Remark}
\newtheorem{example}[theorem]{Example}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{hyperref}
\hypersetup{colorlinks=true,allcolors=red,allbordercolors={1 0 0}}
\usepackage{fontspec}
\setmonofont{JuliaMono-Regular.ttf}[
  BoldFont=JuliaMono-Bold.ttf,
  ItalicFont=JuliaMono-RegularItalic.ttf,
  BoldItalicFont=JuliaMono-BoldItalic.ttf,
  Scale=MatchLowercase
]
\setmathfont{latinmodern-math.otf}
```
