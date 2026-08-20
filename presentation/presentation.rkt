#lang slideshow ; or slideshow/widescreen

; TODO: make all links clickable
; TODO: looks like trying to render code directly here is futile; current workaround I'm using is, take screenshot of the code

(require racket/draw)
(require slideshow/text)

; For 20 minute talk, aim for 10-25 slides ; err towards lower side right now, eg. another talk proposal i saw has total 13 slides
; so mine is good - currently has 14 slides

; We're starting presentation with --keep-titlebar which reduces the height of the window, and slide #:title starts getting cut off
; So increase margin from top of whole slide to compensate
(set-margin! 40)

;;;;;;;;; ENABLE PAGE NUMBER ;;;;;;;;;;;;;

;;; (set-page-numbers-visible! #t)
;;; (current-page-number-font
;;;  (make-font #:size 40
;;;             #:family 'default
;;;             #:weight 'bold))
;;; (current-page-number-adjust
;;;  (lambda (default-string slide-number)
;;;    (format "Slide ~a" slide-number)))

(define original-assembler
  (current-slide-assembler))
(define slide-number 0)

(current-slide-assembler
 (lambda (title title-sep content)
   (set! slide-number (add1 slide-number))
   (define slide-pict
     (original-assembler title title-sep content))
   (define number-pict
     (small (t (number->string slide-number))))

   ;; Put the number in the horizontal center, with a bottom-margin to push up page number so it doesn't disappear in --keep-titlebar mode
   (define bottom-margin 15)          ; pixels
   (pin-over
    slide-pict
    (/ (- (pict-width slide-pict)
          (pict-width number-pict))
       2)
    (- (pict-height slide-pict)
       (pict-height number-pict)
       bottom-margin)
    number-pict)))

;;;;;;;;;;;;;;;;; END ENABLE PAGE NUMBER ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; (t "text") is normal sans-serif font, (tt "code") is monospaced font

(define (bullets . items)
	(apply vl-append 12
				 (map (lambda (item)
								(hc-append 14 (t "-" ) (t item)))
						 items)))

(slide
 #:title "Building a Jupyter Kernel"
 (t "How Python can bring another language to the notebook")
 (blank 0 24)
 (t "Using case study of IForth - a kernel for Forth language"))

; TODO:MAYBE I think later (in actual talk) replace this whole slide with just a live demo
(slide
 #:title "Jupyter Notebook Examples - Python and Forth"
 (vc-append 20
            (scale (bitmap "images/jupyter_python_example.png") 0.7)
            (scale (bitmap "images/jupyter_forth_example.png") 0.7)))

; multi-line string (preserves newline characters)
; standard double quoted string can also be written directly as multi-line, but this way using Here doc avoids need to escape forward slash (would otherwise need to write them as \\)
; double quoted multi line string example:
; "A string
;  having 2
;  or more lines"
;;; (define forth-example-tt #<<HERE
;;;         \ This is a comment.

;;;         \ All programming in Forth is done by manipulating the stack.
;;;         5 2 3 56 76 23 65    \ ok
;;;         \ Those numbers get added to the stack, from left to right.
;;;         .s    \ <7> 5 2 3 56 76 23 65 ok

;;;         \ Functions (called 'words' in Forth) work by manipulating data on the stack.
;;;         5 4 +    \ ok
;;;         \ `.` pops the top result from the stack.
;;;         .    \ 9 ok
;;; HERE
;;; )

(slide
 #:title "Forth in 30 seconds"
 (scale (bitmap "images/jupyter_forth_demo.png") 0.7)
 (blank 0 18)
 (t "See more syntax examples: https://learnxinyminutes.com/forth"))

(slide
 #:title "The message flow"
 (scale (bitmap "images/jupyter_architecture.png") 0.6)
 (blank 0 8)
 (with-size 18
   (vl-append 8
     (para "The Jupyter Server communicates with the kernel over 5 ZeroMQ channels:")
     (item "Shell: Main request/reply loop, frontend sends code to run here.")
     (item "IOPub: Broadcast channel. Kernel can publish stdout, stderr, HTML, etc.")
     (item "Stdin: Kernel can request user input.")
     (item "Control: High-priority commands (eg. Shutdown, Interrupt) that bypass execution queue.")
     (item "Heartbeat: Simple ping/pong socket, check kernel is still alive.")
     (blank 0 6)
     (with-size 14
       (t "Source: https://www.datahaskell.org/blog/2025/11/25/a-tale-of-two-kernels.html#the-jupyter-kernel-architecture")))))

(slide
 #:title "Subclass Jupyter Kernel"
 (scale (bitmap "images/IForth_code.png") 0.6))  ; used 0.6 scale to make the image fit inside slide without pushing out the slide number at the bottom

(slide
 #:title "Register the custom kernel with Jupyter"
 (scale (bitmap "images/install_kernelspec.png") 0.7))

(slide
 #:title "Unit Test using module jupyter_kernel_test"
 (scale (bitmap "images/kernel_unit_test.png") 0.7))

(slide
 #:title 
 (t "Check out IForth for an example Jupyter kernel implementation.")
 (t "And maybe try Forth - it's an interesting language :)")
 (tt "Repo: https://github.com/sohang3112/iforth")
 (blank 0 15)
 (t "Thank You!")
 (blank 0 15)
 (small (t "PS: This presentation was made using https://docs.racket-lang.org/slideshow/"))
 (blank 0 15)
 (t "Questions?"))