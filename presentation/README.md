Using Racket's `slideshow` library to generate presentation.

* Full-screen immediate presentation: `slideshow --keep-titlebar presentation.rkt`. Navigate slides using left, right arrow keys. Quit using Esc key.
  * Added `--keep-titlebar` to avoid the default full-screen.
* Save presentation as PDF file: `slideshow --pdf -o presentation.pdf presentation.rkt`

**Resources**:
- Hello World presentation: https://docs.racket-lang.org/slideshow/Creating_Slide_Presentations.html#(part._.Slide_.Basics)
