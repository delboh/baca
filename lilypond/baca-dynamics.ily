%%% NOTE: Use ...
%%%
%%%       DynamicText.X-extent = #'(0 . 0)
%%%
%%% ... instead of ...
%%%
%%%       DynamicText.X-extent = ##f
%%%
%%% ... to avoid warnings in LilyPond log.

%%% ANCORA DYNAMICS %%%

#(define-markup-command
    (baca-ancora-dynamic layout props dynamic)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #dynamic
        \hspace #0.25
        \normal-text ancora
        }
    #}))

baca-ppp-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "ppp")
    )

baca-pp-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "pp")
    )

baca-p-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "p")
    )

baca-mp-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "mp")
    )

baca-mf-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "mf")
    )

baca-f-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "f")
    )

baca-ff-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "ff")
    )

baca-fff-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "fff")
    )

%%% COMPOSITE DYNAMICS %%%

baca-pppf = #(make-dynamic-script "pppf")

baca-pppff = #(make-dynamic-script "pppff")

baca-pppfff = #(make-dynamic-script "pppfff")


baca-ppf = #(make-dynamic-script "ppf")

baca-ppff = #(make-dynamic-script "ppff")

baca-ppfff = #(make-dynamic-script "ppfff")


baca-pf = #(make-dynamic-script "pf")

baca-pff = #(make-dynamic-script "pff")

baca-pfff = #(make-dynamic-script "pfff")

%%% COMPOSITE DYNAMICS (WITH DELIMITER) %%%

#(define-markup-command
    (baca-delimited-composite-dynamic layout props left right)
    (string? string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #left
        \hspace #-0.625
        \general-align #Y #-0.5
        \scale #'(2 . 2)
        \normal-text
        "/"
        \hspace #-0.625
        \dynamic #right
        }
    #}))

% from ppp

baca-ppp-pp = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "ppp" "pp")
    )

baca-ppp-p = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "ppp" "p")
    )

baca-ppp-mp = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "ppp" "mp")
    )

baca-ppp-mf = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "ppp" "mf")
    )

baca-ppp-f = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "ppp" "f")
    )

baca-ppp-ff = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "ppp" "ff")
    )

baca-ppp-fff = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "ppp" "fff")
    )

% from pp

baca-pp-ppp = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "pp" "ppp")
    )

baca-pp-p = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "pp" "p")
    )

baca-pp-mp = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "pp" "mp")
    )

baca-pp-mf = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "pp" "mf")
    )

baca-pp-f = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "pp" "f")
    )

baca-pp-ff = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "pp" "ff")
    )

baca-pp-fff = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "pp" "fff")
    )

% from p

baca-p-ppp = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "p" "ppp")
    )

baca-p-pp = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "p" "pp")
    )

baca-p-mp = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "p" "mp")
    )

baca-p-mf = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "p" "mf")
    )

baca-p-f = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "p" "f")
    )

baca-p-ff = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "p" "ff")
    )

baca-p-fff = #(
    make-dynamic-script 
    (markup #:baca-delimited-composite-dynamic "p" "fff")
    )

%%% EFFORT DYNAMICS %%%

#(define-markup-command
    (baca-effort-dynamic layout props left dynamic right)
    (number? string? number?)
    (interpret-markup layout props
    #{
    \markup
    \whiteout
    \line {
        \general-align #Y #-2 \normal-text \larger "“"
        \hspace #left
        \dynamic #dynamic
        \hspace #right
        \general-align #Y #-2 \normal-text \larger "”"
        }
    #}))

baca-effort-ppp = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "ppp" -0.25)
    )

baca-effort-pp = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "pp" -0.25)
    )

baca-effort-p = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "p" -0.25)
    )

baca-effort-mp = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "mp" -0.25)
    )

baca-effort-mf = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "mf" -0.2)
    )

baca-effort-f = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.4 "f" -0.2)
    )

baca-effort-ff = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.4 "ff" -0.2)
    )

baca-effort-fff = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.4 "fff" -0.2)
    )

baca-effort-sfz = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.3 "sfz" -0.2)
    )

baca-effort-sffz = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.3 "sffz" -0.2)
    )

%%% EFFORT DYNAMICS (PARENTHESIZED) %%%

baca-effort-ppppp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:baca-effort-dynamic -0.1 "ppppp" -0.25
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-effort-pppp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:baca-effort-dynamic -0.1 "pppp" -0.25
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-effort-ppp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:baca-effort-dynamic -0.1 "ppp" -0.25
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-effort-pp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:baca-effort-dynamic -0.1 "pp" -0.25
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-effort-p-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:baca-effort-dynamic -0.1 "p" -0.25
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-effort-mp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.45
            #:baca-effort-dynamic -0.1 "mp" -0.25
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-effort-mf-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.45
            #:baca-effort-dynamic -0.1 "mf" -0.2
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-effort-f-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:baca-effort-dynamic -0.4 "f" -0.2
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-effort-ff-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:baca-effort-dynamic -0.4 "ff" -0.2
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-effort-fff-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:baca-effort-dynamic -0.4 "fff" -0.2
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-effort-ffff-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:baca-effort-dynamic -0.4 "ffff" -0.2
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-effort-fffff-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:baca-effort-dynamic -0.4 "fffff" -0.2
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

%%% FP DYNAMICS %%%

baca-ffp = #(make-dynamic-script "ffp")

baca-fffp = #(make-dynamic-script "fffp")

%%% PARENTHESIZED DYNAMICS %%%

baca-ppppp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:dynamic "ppppp"
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-pppp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:dynamic "pppp"
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-ppp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:dynamic "ppp"
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-pp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:dynamic "pp"
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-p-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.25
            #:dynamic "p"
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-mp-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.45
            #:dynamic "mp"
            #:hspace -0.625
            #:normal-text ")"
            )
        )
    )

baca-mf-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.45
            #:dynamic "mf"
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-f-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:dynamic "f"
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-ff-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:dynamic "ff"
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-fff-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:dynamic "fff"
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-ffff-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:dynamic "ffff"
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

baca-fffff-parenthesized = #(
    make-dynamic-script
    (markup
        #:line (
            #:normal-text "("
            #:hspace -0.15
            #:dynamic "fffff"
            #:hspace 0
            #:normal-text ")"
            )
        )
    )

%%% POCO SCRATCH DYNAMICS %%%

#(define-markup-command
    (baca-poco-scratch-dynamic layout props dynamic)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #dynamic
        \hspace #0.25
        \normal-text poco
        \normal-text scratch
        }
    #}))

baca-ppp-poco-scratch = #(
    make-dynamic-script
    (markup #:baca-poco-scratch-dynamic "ppp")
    )

baca-pp-poco-scratch = #(
    make-dynamic-script
    (markup #:baca-poco-scratch-dynamic "pp")
    )

baca-p-poco-scratch = #(
    make-dynamic-script
    (markup #:baca-poco-scratch-dynamic "p")
    )

baca-mp-poco-scratch = #(
    make-dynamic-script
    (markup #:baca-poco-scratch-dynamic "mp")
    )

baca-mf-poco-scratch = #(
    make-dynamic-script
    (markup #:baca-poco-scratch-dynamic "mf")
    )

baca-f-poco-scratch = #(
    make-dynamic-script
    (markup #:baca-poco-scratch-dynamic "f")
    )

baca-ff-poco-scratch = #(
    make-dynamic-script
    (markup #:baca-poco-scratch-dynamic "ff")
    )

baca-fff-poco-scratch = #(
    make-dynamic-script
    (markup #:baca-poco-scratch-dynamic "fff")
    )

%%% POSS. DYNAMICS %%%

#(define-markup-command
    (baca-poss-dynamic layout props dynamic)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #dynamic
        \hspace #0.25
        \normal-text poss.
        }
    #}))

baca-ppp-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "ppp")
    )

baca-pp-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "pp")
    )

baca-p-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "p")
    )

baca-f-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "f")
    )

baca-ff-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "ff")
    )

baca-fff-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "fff")
    )

%%% SEMPRE DYNAMICS %%%

#(define-markup-command
    (baca-sempre-dynamic layout props dynamic)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #dynamic
        \hspace #0.25
        \normal-text sempre
        }
    #}))

baca-pppp-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "pppp")
    )

baca-ppp-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "ppp")
    )

baca-pp-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "pp")
    )

baca-p-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "p")
    )

baca-mp-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "mp")
    )

baca-mf-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "mf")
    )

baca-f-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "f")
    )

baca-ff-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "ff")
    )

baca-fff-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "fff")
    )

%%% SCRATCH DYNAMICS %%%

#(define-markup-command
    (baca-scratch-dynamic layout props dynamic)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #dynamic
        \hspace #0.25
        \normal-text scratch
        }
    #}))

baca-ppp-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "ppp")
    )

baca-pp-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "pp")
    )

baca-p-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "p")
    )

baca-mp-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "mp")
    )

baca-mf-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "mf")
    )

baca-f-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "f")
    )

baca-ff-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "ff")
    )

baca-fff-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "fff")
    )

%%% SFORZANDO DYNAMICS %%%

baca-sff = #(make-dynamic-script "sff")
baca-sffp = #(make-dynamic-script "sffp")
baca-sffpp = #(make-dynamic-script "sffpp")
baca-sfpp = #(make-dynamic-script "sfpp")
baca-sffz = #(make-dynamic-script "sffz")
baca-sfffz = #(make-dynamic-script "sfffz")

baca-sfz-f = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "sfz"
            #:hspace -0.25
            #:normal-text "/"
            #:hspace -0.5
            #:dynamic "f"
            )
        )
    )

baca-sfz-p = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "sfz"
            #:hspace 0
            #:normal-text "/"
            #:hspace 0 
            #:dynamic "p"
            )
        )
    )

%%% SUBITO DYNAMICS %%%

baca-ppp-sub = 
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "ppp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-pp-sub = 
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "pp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-p-sub = 
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "p"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-mp-sub = 
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "mp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-mf-sub =
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "mf"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-f-sub =
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "f"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-ff-sub =
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "ff"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-fff-sub =
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "fff"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

%%% SUB. EFFORT DYNAMICS %%%

#(define-markup-command
    (baca-effort-sub-dynamic layout props left dynamic right)
    (number? string? number?)
    (interpret-markup layout props
    #{
    \markup
    \whiteout
    \line {
        \general-align #Y #-2 \normal-text \larger "“"
        \hspace #left
        \dynamic #dynamic
        \hspace #right
        \general-align #Y #-2 \normal-text \larger "”"
        \hspace #0.25
        \normal-text sub.
        }
    #}))

baca-ppp-effort-sub = #(
    make-dynamic-script
    (markup #:baca-effort-sub-dynamic -0.1 "ppp" -0.25)
    )

baca-pp-effort-sub = #(
    make-dynamic-script
    (markup #:baca-effort-sub-dynamic -0.1 "pp" -0.25)
    )

baca-p-effort-sub = #(
    make-dynamic-script
    (markup #:baca-effort-sub-dynamic -0.1 "p" -0.25)
    )

baca-mp-effort-sub = #(
    make-dynamic-script
    (markup #:baca-effort-sub-dynamic -0.1 "mp" -0.25)
    )

baca-mf-effort-sub = #(
    make-dynamic-script
    (markup #:baca-effort-sub-dynamic -0.1 "mf" -0.2)
    )

baca-f-effort-sub = #(
    make-dynamic-script
    (markup #:baca-effort-sub-dynamic -0.4 "f" -0.2)
    )

baca-ff-effort-sub = #(
    make-dynamic-script
    (markup #:baca-effort-sub-dynamic -0.4 "ff" -0.2)
    )

baca-fff-effort-sub = #(
    make-dynamic-script
    (markup #:baca-effort-sub-dynamic -0.4 "fff" -0.2)
    )

%%% TEXT-ONLY DYNAMICS %%%

baca-appena-udibile = 
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:normal-text "appena udibile"
            )
        )
    )

baca-niente = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:normal-text
        #:italic "niente"
        )
    )

%%% TEXTUAL DYNAMICS %%%

baca-p-sub-but-accents-continue-sffz = 
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -0.75 #:dynamic "p"
            #:normal-text "sub. (but accents continue"
            #:dynamic "sffz"
            #:hspace -0.5
            #:normal-text ")"
            )
        )
    )

baca-f-but-accents-sffz =
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -0.75 #:dynamic "f"
            #:hspace 0.25
            #:normal-text "(but accents"
            #:hspace 0.25
            #:dynamic "sffz"
            #:hspace -0.5
            #:normal-text ")"
            )
        )
    )

baca-f-sub-but-accents-continue-sffz =
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -0.75 #:dynamic "f"
            #:hspace 0.25
            #:normal-text "sub. (but accents continue"
            #:dynamic "sffz"
            #:hspace -0.5
            #:normal-text ")"
            )
        )
    )
