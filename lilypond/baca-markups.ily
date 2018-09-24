%%% BOWSTROKE MARKUP %%%

baca-full-downbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.downbow"
    \path #0.15
    #'(
        (moveto 0.7375 0.05)
        (rlineto 1 0)
        (closepath)
        )

baca-full-upbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.upbow"
    \path #0.15
    #'(
        (moveto 0.62 2.005)
        (rlineto 1 0)
        (closepath)
        )

baca-stop-on-string-markup =
    \markup
    \path #0.15
    #'(
        (moveto 0 0)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )

baca-stop-on-string-full-downbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.downbow"
    \path #0.15
    #'(
        (moveto 0.7375 0.05)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )

baca-stop-on-string-full-upbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.upbow"
    \path #0.15
    #'(
        (moveto 0.62 2.005)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )

%%% CIRCLE BOWING MARKUP %%%

baca-circle-bowing-markup =
    \markup
    \translate #'(0.6 . 0)
    \scale #'(0.35 . 0.35)
    \concat {
        \draw-circle #2 #0.4 ##f
        \hspace #-4.5
        \raise #0.75
        \with-color #white
        \scale #'(0.35 . 0.35)
        \draw-circle #1 #1 ##t
        \hspace #-1.5
        \raise #-0.75
        \scale #'(0.75 . 0.75)
        \triangle ##t
        \hspace #-1
        \raise #1.35
        \with-color #white
        \rotate #45
        \filled-box #'(-0.35 . 0.35) #'(-0.35 . 0.35) #0
    }

%%% DAMP MARKUP %%%

baca-damp-markup =
    \markup
    \scale #'(0.75 . 0.75)
    \combine
    \bold
    \override #'(font-name . "Times") "O"
    \path #0.15
    #'(
        (moveto -.4 .7)
        (rlineto 2.4 0)
        (closepath)
        (moveto .8 -.5)
        (rlineto 0 2.4)
        )

baca-damp-half-clt-markup =
    \markup
    \raise #0.25
    \line {
        \baca-damp-markup
        "½ clt"
    }

%%% DIAMOND MARKUP %%%

baca-black-diamond-markup =
    \markup
    \musicglyph #"noteheads.s2harmonic"

baca-diamond-markup =
    \markup
    \musicglyph #"noteheads.s0harmonic"

baca-diamond-parenthesized-double-diamond-markup =
    \markup
    \concat {
        \general-align #Y #2.5
        \scale #'(0.75 . 0.75)
        \musicglyph #"noteheads.s0harmonic"
        \hspace #0.45
        \general-align #Y #1
        \scale #'(1 . 1.5)
        "("
        \hspace #-0.1
        \general-align #Y #1.25
        \override #'(baseline-skip . 1.75)
        \scale #'(0.75 . 0.75)
        \column
        {
            \musicglyph #"noteheads.s0harmonic"
            \musicglyph #"noteheads.s0harmonic"
        }
        \hspace #-0.15
        \general-align #Y #1
        \scale #'(1 . 1.5)
        ")"
    }

baca-double-black-diamond-markup =
    \markup
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s2harmonic"
        \musicglyph #"noteheads.s2harmonic"
    }

baca-double-diamond-markup =
    \markup
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s0harmonic"
        \musicglyph #"noteheads.s0harmonic"
    }

baca-triple-diamond-parenthesized-top-markup =
    \markup
    \concat {
        \general-align #Y #1.25
        \override #'(baseline-skip . 1.75)
        \scale #'(0.75 . 0.75)
        \center-column
        {
            \concat {
                \general-align #Y #0.75
                "("
                \general-align #Y #1
                \musicglyph #"noteheads.s0harmonic"
                \general-align #Y #0.75
                ")"
                }
            \musicglyph #"noteheads.s0harmonic"
            \musicglyph #"noteheads.s0harmonic"
        }
        \hspace #-0.15
    }

baca-triple-black-diamond-markup =
    \markup
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s2harmonic"
        \musicglyph #"noteheads.s2harmonic"
        \musicglyph #"noteheads.s2harmonic"
    }

baca-triple-diamond-markup =
    \markup
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s0harmonic"
        \musicglyph #"noteheads.s0harmonic"
        \musicglyph #"noteheads.s0harmonic"
    }

%%% FERMATA MARKUP %%%

baca-fermata-markup =
    \markup
    \with-dimensions-from \null
    \musicglyph #"scripts.ufermata"

baca-long-fermata-markup = \markup
    \with-dimensions-from \null
    \musicglyph #"scripts.ulongfermata"

baca-short-fermata-markup =
    \markup
    \with-dimensions-from \null
    \musicglyph #"scripts.ushortfermata"

baca-very-long-fermata-markup =
    \markup
    \with-dimensions-from \null
    \musicglyph #"scripts.uverylongfermata"

%%% REHEARSAL MARKS %%%

% IMPORTANT: markup attach direction must be neutral or down (- or _);
%            markup attach direction of up (^) negatively impacts global
%            skips context vertical spacing
baca-rehearsal-mark-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \tweak font-size #10
    - \markup
    \with-dimensions-from \null
    \override #'(box-padding . 0.5)
    \box
    { #string }
    #}
    )
