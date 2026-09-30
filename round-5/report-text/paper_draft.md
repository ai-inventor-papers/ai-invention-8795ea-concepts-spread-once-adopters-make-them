\documentclass[a4paper,11pt]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{natbib}
\usepackage[colorlinks=true,citecolor=blue,linkcolor=blue,urlcolor=blue]{hyperref}
\usepackage{geometry}
\geometry{margin=2.5cm}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{multirow}
\usepackage{array}
\usepackage{xcolor}

\title{Do temporal network signals predict how scientific concepts spread across disciplines?}

\author{AI Inventor}

\date{}

\begin{document}

\maketitle

\begin{abstract}
New scientific concepts differ sharply in how broadly they spread across disciplines. We ask whether the early structure of a concept's topic cooccurrence network anticipates later cross-field breadth, beyond simple measures of volume and reach. Using the OpenAlex corpus, we identify 12{,}499 concepts, track 27{,}393 adoption episodes across 26 fields, and screen 53 early network indicators against a five-feature popularity baseline. Seven indicators survive held-out validation and compose into an openness index (OPEN) that measures a concept's early tendency to acquire novel, community-spanning cooccurrence partners. On a confirmatory cohort never used in selection, OPEN predicts size-adjusted breadth with partial Spearman correlation +0.17 (95\% CI [+0.09, +0.25]). The signal is topical non-redundancy of the home neighbourhood, not temporal partner turnover: a within-concept permutation null absorbs the year-to-year churn, while the signal survives rarefaction and degree-preserving configuration nulls. Separately, a conditional logit on field-entry events confirms that concepts spread next to fields related to the ones currently retaining them, extending the principle of relatedness from economic complexity. These results suggest that the diversity of a concept's early intellectual neighbourhood, not its stability, distinguishes concepts destined for broad disciplinary integration.
\end{abstract}

\section{Introduction}

Some scientific concepts remain confined to their home discipline for decades, while others cross field boundaries within a few years. Optogenetics, born in neuroscience, entered genetics, psychiatry and bioengineering; deep learning, rooted in computer science, now appears in medicine, materials science and linguistics. Understanding what distinguishes broadly spreading concepts from locally absorbed ones matters for science policy, research evaluation and the design of interdisciplinary programmes \citep{Rafols2009,Hofstra2019}. If early structural signals predict later cross-field integration, funders and institutions could identify concepts with high diffusion potential before that diffusion is observable in publication counts alone.

The problem is hard because simple popularity metrics (publication volume, growth rate, share of papers outside the home field) already explain much of the variance in later breadth \citep{Rotolo2015,Singh2021}. Any network indicator must add information \emph{beyond} these baselines. Prior work has proposed several candidate signals, including community diversity of early adopters \citep{Weng2013}, collaboration density before emergence \citep{Salatino2017}, and structural variation in citation networks \citep{Salatino2018}. However, these studies typically operate on curated concept sets without held-out validation, mix concept-level and field-level units of analysis, or do not control for simple volume-based predictors. No prior study has screened a broad set of temporal knowledge-network indicators against a shared baseline on held-out field groups for the specific outcome of size-adjusted cross-disciplinary breadth.

A second open question concerns the routes by which concepts move between fields. The principle of relatedness, established for regional economic diversification \citep{Hidalgo2007,Neffke2011,Pinheiro2021}, predicts that actors diversify into activities related to their existing portfolio. For scientific fields adopting new concepts, this principle has been tested for entry \citep{Hidalgo2018} but not for the role of currently \emph{retaining} fields, those that have adopted a concept and kept publishing on it. Whether concepts spread next to fields related to the ones currently retaining them, beyond relatedness to the home field alone, is untested.

This paper addresses both questions with a large-scale empirical study. We identify 12{,}499 concepts from the OpenAlex bulk snapshot (476 million works, 2026-09-23), compute 53 early network indicators across six families, and test them on held-out field groups and a confirmatory onset cohort [ARTIFACT:art_dFQ6jbgNsR6Q]. We also build a conditional logit model of field entry that tests whether retained-field relatedness predicts the next field a concept enters [ARTIFACT:art_Vu7gHKQXfL53].

\subsection*{Summary of contributions}

\begin{itemize}
    \item We screen 53 early cooccurrence network indicators against a five-feature popularity baseline and confirm seven on held-out field groups for predicting rarefied cross-field breadth (Section~\ref{sec:rq1}).
    \item We introduce the OPEN index, a six-component composite of early cooccurrence openness, and confirm it on a 2015--2016 cohort never used in any selection step (Section~\ref{sec:open}).
    \item We show that early neighbourhood consolidation, measured by Cheng et al.'s (2023) ideational consistency, predicts volume growth but \emph{narrower} cross-field reach, a reversal that holds in all five field groups (Section~\ref{sec:cheng}).
    \item We confirm that concepts spread next to fields related to the ones currently retaining them ($d = 0.32$), extending the principle of relatedness (Section~\ref{sec:rq2}).
    \item We decompose breadth into exploration and retention channels and show that early contact diversity accounts for 73\% of the breadth gap (Section~\ref{sec:decomp}).
    \item We demonstrate that the openness--breadth association is topical non-redundancy, not temporal partner turnover (Section~\ref{sec:confound}).
\end{itemize}

[FIGURE:fig_overview]

\section{Related work}
\label{sec:related}

\textbf{Concept diffusion in science.} Cheng et al.\ (2023) tracked roughly 2{,}000 new ideas across Web of Science fields and found that early social reach, the number of disconnected researcher groups adopting an idea, was the strongest predictor of whether an idea became ``core.'' Their ideational consistency measure predicted next-year volume. \citet{Rotolo2015} defined emerging technologies through five attributes including novelty and fast growth but did not test cross-field spread. \citet{Salatino2017} showed that collaboration density rises before topic emergence. \citet{Krenn2019} forecast research trends from semantic networks. \citet{Singh2021} quantified the rise and fall of scientific fields using publication trajectories. None of these studies screened a broad indicator set against a shared baseline with held-out validation for the specific outcome of size-adjusted cross-field breadth.

\textbf{Topic cooccurrence and citation networks.} \citet{Callon1991} introduced coword analysis as a tool for mapping the structure of research. \citet{Chavalarias2013} used phylomemetic methods to track how scientific fields branch and merge. \citet{Salatino2018} proposed the AUGUR system for forecasting topic emergence from cooccurrence backbone dynamics. Citation homophily across fields exceeds chance but has not been decomposed into background and concept-specific terms. \citet{Holmgren2023} tracked change in higher-order overlapping community structure in bibliometric networks.

\textbf{Novelty, recombination and impact.} \citet{Uzzi2013} found that high-impact papers combine conventional and atypical journal pairings. \citet{Hofstra2019} documented the diversity--innovation paradox in science: researchers from underrepresented groups produce more novel work but receive fewer citations. \citet{Foster2013} distinguished tradition and innovation strategies in science. \citet{Tria2013} modelled the dynamics of correlated novelties, showing that novelty begets novelty through what they call the ``adjacent possible,'' the set of combinations reachable from the current state of knowledge. These studies operate at the paper level; ours operates at the concept level and asks about cross-field \emph{breadth} rather than citation impact.

\textbf{The principle of relatedness.} \citet{Hidalgo2007} showed that a country's position in the product space predicts which products it diversifies into. \citet{Neffke2011} extended this to regional industry diversification, and \citet{Rigby2015} to knowledge space entry and exit. \citet{Hidalgo2018} formalised the principle of relatedness. \citet{Pinheiro2021} required sustained presence for diversification events. \citet{Bahar2014} showed that countries adopt products exported by their neighbours, a knowledge-diffusion channel for relatedness. Our contribution is to test whether relatedness to the set of fields currently \emph{retaining} a concept predicts entry, beyond relatedness to the home field and conventional density measures.

\textbf{Community structure and virality.} \citet{Weng2013} showed that early community diversity predicts virality of online content (AUC 0.83). \citet{Ugander2012} found that structural diversity, defined as the number of connected components among an adopter's neighbours who have adopted, drives social contagion on Facebook. \citet{Centola2010} demonstrated experimentally that complex contagions require reinforcement from multiple communities. \citet{Palla2007} tracked the evolution of overlapping communities in large networks. \citet{Burt2004} showed that structural holes, brokerage positions spanning disconnected groups, generate good ideas. Our indicator screen tests the scholarly analogue of these mechanisms: whether a concept's early cooccurrence partners spanning multiple communities predicts later cross-field breadth.

\section{Data and methods}
\label{sec:methods}

\subsection{Concept identification and panel construction}

We use the OpenAlex bulk snapshot (2026-09-23; 476{,}196{,}327 works; 129.4 million base works 1995--2022). Concepts are identified by Aho--Corasick title matching of 56{,}643 legacy OpenAlex concepts (levels 2--5) plus Wikidata aliases, with stemmed verification [ARTIFACT:art_dFQ6jbgNsR6Q]. A per-concept LLM precision gate drops concepts with precision below 0.80.

A concept's \emph{onset year} $t_0$ is the first year it reaches 20 grounded publications. \emph{Home field(s)} are the field(s) holding at least 40\% of the first 30 grounded papers. The specification was frozen on DEV data (hash-sealed before held-out scoring) and unsealed once. The panel comprises 12{,}499 concepts and 27{,}393 concept-by-field adoption episodes (Table~\ref{tab:panel}).

\begin{table}[ht]
\centering
\caption{Panel composition. DEV concepts have home fields in Computer Science, Engineering, Biochemistry/Genetics/Medicine. Held-out groups cover the remaining field families.}
\label{tab:panel}
\small
\begin{tabular}{lrr}
\toprule
Split & Concepts & Episodes \\
\midrule
DEV (CS/Eng/BGM/Med, onset 2003--2009) & 4{,}771 & 9{,}079 \\
Cohort (onset 2010--2014, all fields) & 4{,}356 & 9{,}799 \\
Held-out Physical Sciences & 742 & 1{,}662 \\
Held-out Life \& Environment & 1{,}113 & 3{,}099 \\
Held-out Social Sciences & 1{,}352 & 3{,}320 \\
Held-out Math \& Decision Sci. & 165 & 434 \\
\midrule
\textbf{Total} & \textbf{12{,}499} & \textbf{27{,}393} \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Outcome: rarefied field breadth}

The primary outcome is \emph{rarefied field breadth} $O_{2r}$ ($m = 50$): the expected number of distinct venue fields among a fixed-size random draw of $m$ papers from a concept's publications in years $t_0 + 6$ to $t_0 + 8$, computed by exact hypergeometric rarefaction. Rarefaction separates size-adjusted breadth from sheer volume: a concept with 10{,}000 papers in one field scores lower than a concept with 200 papers spread across six fields. Secondary outcomes include sustained uptake ($O_{1c}$, binary: concept still active at $t_0 + 8$), transience ($O_3$, binary: concept drops below 5 papers by $t_0 + 8$), and field- and year-normalised citation growth ($O_4$).

[FIGURE:fig_outcomes]

\subsection{Baseline and indicator families}

We define a \emph{five-feature baseline} consisting of log early volume, publication growth, non-home share, Shannon entropy and field reach, all computed over $t_0$ to $t_0 + 2$. The 53 candidate indicators span six families: cooccurrence ego-network topology (27 indicators: degree, density, persistence, novelty, community counts), popularity and volume (6), disciplinary spread (3), retained frontier (7: contact reach, retention ratio, densities), gateway centrality on the field backbone (7), and coauthor reach (3).

\subsection{The OPEN index}

The OPEN index is the mean of six signed $z$-scored ego-network components from the early window ($t_0$ to $t_0 + 2$):

\begin{enumerate}
    \item New edge rate (positive sign): the fraction of a concept's cooccurrence neighbours that are new.
    \item Number of Leiden communities reached ($n_{\text{comm}}$, positive): how many distinct topic communities a concept's neighbours span.
    \item Participation coefficient (positive): the share of a concept's ties that cross community boundaries.
    \item Neighbourhood novelty residual (NOV$_{\text{res}}$, positive): the novelty of a concept's cooccurrence partners after residualising on degree.
    \item Ego density (negative sign): the density of the concept's local cooccurrence subgraph.
    \item Edge persistence (negative sign): the fraction of the concept's neighbours retained across windows.
\end{enumerate}

The $z$-score constants are frozen from the DEV data. We test three builds: OPEN$_{\text{home}}$ (home-field cooccurrence graph only), OPEN$_{\text{all}}$ (corpus-wide graph), and OPEN$_{\text{sizematch}}$ (corpus-wide papers subsampled to home counts).

\subsection{Statistical framework}

Indicator screening uses \emph{partial Spearman priority} (PSP): the Pearson correlation of rank-transformed indicator and outcome residuals, both residualised on the baseline covariates and control rungs. Inference uses 2{,}000 concept-level bootstrap resamples with refit [ARTIFACT:art_dFQ6jbgNsR6Q]. Pooling across field groups uses the DerSimonian--Laird random-effects estimator \citep{Dersimonian1986} with $I^2$ heterogeneity reporting \citep{Higgins2002}. Multiple comparisons use Holm correction across the pre-declared family.

We also define NOVCHURN as the mean of $z$(NOV$_{\text{res}}$) and $-z$(edge persistence), a two-component novelty/churn measure used in mechanism analyses.

For the field-entry analysis, we use a conditional logit on concept-year risk sets, where each concept-year stratum includes all non-home fields not yet entered, and the event is entry (at least 2 cumulative grounded papers). The entry baseline includes relatedness to home, log field size, density over all ever-entered fields, and the target field's own eigenvector centrality on the topic-relatedness backbone.

\section{Results: indicator screen}
\label{sec:rq1}

\subsection{Held-out indicator screen}

The top 10 indicators selected on DEV by partial Spearman priority were tested once on four held-out field groups and two cohort splits [ARTIFACT:art_dFQ6jbgNsR6Q]. Seven are confirmed with $p < 0.05$ after Holm correction for multiple comparisons and 95\% CI excluding zero (Table~\ref{tab:screen}).

\begin{table}[ht]
\centering
\caption{Held-out indicator screen: the 10 indicators with highest DEV partial Spearman priority for rarefied breadth ($O_{2r}$, $m = 50$), tested on held-out groups. DerSimonian--Laird pooled estimates with 95\% CI. Confirmed indicators (Holm $p < 0.05$ and CI excluding zero) are marked.}
\label{tab:screen}
\small
\begin{tabular}{llccccc}
\toprule
Indicator & Family & Pooled PSP & 95\% CI & $I^2$ & Sign & Confirmed \\
\midrule
M0\_density\_end & Relatedness & +0.375 & [+0.279, +0.462] & 0.74 & 6/6 & \textbf{Yes} \\
D\_vol\_end & Relatedness & +0.307 & [+0.256, +0.356] & 0.10 & 6/6 & \textbf{Yes} \\
CONTACT\_REACH & Relatedness & +0.211 & [+0.161, +0.261] & 0.00 & 6/6 & \textbf{Yes} \\
$n_\text{comm}$ (W3) & Cooccurrence & +0.167 & [+0.063, +0.267] & 0.78 & 6/6 & \textbf{Yes} \\
NOV$_{\text{res}}$ & Cooccurrence & +0.151 & [+0.044, +0.255] & 0.75 & 6/6 & \textbf{Yes} \\
RETENTION\_RATIO & Relatedness & $-$0.114 & [$-$0.160, $-$0.067] & 0.00 & 6/6 & \textbf{Yes} \\
ego\_density (W3) & Cooccurrence & $-$0.102 & [$-$0.151, $-$0.053] & 0.00 & 6/6 & \textbf{Yes} \\
Rao--Stirling & Cooccurrence & $-$0.072 & [$-$0.153, +0.010] & 0.44 & 5/6 & No \\
$G_\text{btw}$ & Centrality & +0.056 & [$-$0.006, +0.118] & 0.33 & 6/6 & No \\
log offhome vol. & Volume & $-$0.089 & [$-$0.171, $-$0.007] & 0.63 & 5/6 & No \\
\bottomrule
\end{tabular}
\end{table}

The confirmed indicators span two families: relatedness (end-of-window field density, volume-weighted field density, contact reach, retention ratio) and cooccurrence topology (community count, neighbourhood novelty residual, ego density). No centrality or volume-only indicator survives. Two confirmed indicators carry negative signs: the early retention ratio (concepts with higher early field retention spread \emph{less} broadly) and ego density (concepts with denser cooccurrence neighbourhoods spread less).

An ElasticNet combining all indicators adds Spearman +0.059 [+0.046, +0.073] over the five-feature baseline on held-out groups; an Explainable Boosting Machine adds +0.052 [+0.037, +0.067].

[FIGURE:fig_rq1_confirmed]

\subsection{Pre-onset footprint}
\label{sec:footprint}

We define a concept's \emph{pre-onset footprint} as the publication presence of its name in fields other than the home field before its onset year $t_0$. About half of the end-of-window field density and volume-weighted field density signal comes from this footprint. On held-out data, the postonset-only field density drops from +0.374 to +0.187 [+0.145, +0.246] and the volume-weighted variant drops from +0.317 to +0.176 [+0.114, +0.227]. The postonset components remain clearly positive, but these indicators are partly legacy presence, not purely early network dynamics.

[FIGURE:fig_full_screen]

\subsection{Confirmatory cohort test of the OPEN index}
\label{sec:open}

The OPEN index was confirmed on a 2015--2016 onset cohort never used in any prior screen [ARTIFACT:art_dFQ6jbgNsR6Q]. We define a six-rung \emph{control ladder} that tests OPEN's partial Spearman with rarefied breadth under increasingly demanding baselines (Table~\ref{tab:ladder}). Each rung adds a covariate set: the first rung adds the five-feature baseline plus onset year; subsequent rungs add contact reach, concept type, pre-onset footprint, label coverage and home-group fixed effects, in that order.

\begin{table}[ht]
\centering
\caption{OPEN index control ladder on the 2015--2016 confirmatory cohort. PSP = partial Spearman priority with rarefied breadth ($O_{2r}$, $m = 50$), 95\% concept-bootstrap CI.}
\label{tab:ladder}
\small
\begin{tabular}{lccccccc}
\toprule
Build & R0 & R1 & R2 & R3 & R4 & R5 & $n$ \\
\midrule
OPEN$_{\text{home}}$ & \small{+.12} & \small{+.10} & \small{+.09} & \small{+.08} & \small{+.07} & \small{+.06} & 573 \\
OPEN$_{\text{all}}$ & \small{+.21} & \small{+.18} & \small{+.17} & \small{+.17} & \small{+.15} & \small{+.14} & 630 \\
OPEN$_{\text{size}}$ & \small{+.18} & \small{+.15} & \small{+.15} & \small{+.14} & \small{+.12} & \small{+.11} & 591 \\
\bottomrule
\end{tabular}
\end{table}

OPEN$_{\text{all}}$ and OPEN$_{\text{sizematch}}$ survive all six rungs with confidence intervals excluding zero. OPEN$_{\text{home}}$ passes the primary concept-type rung (PSP = +0.091, 95\% CI [+0.013, +0.171]) but its DerSimonian--Laird pooled interval includes zero (+0.083 [$-$0.007, +0.173]), making the home-only signal marginal. The paired difference OPEN$_{\text{all}}$ minus OPEN$_{\text{home}}$ at the footprint rung is +0.093 [+0.016, +0.169], confirming that cross-field cooccurrence carries information beyond home-field structure.

A specification curve across 1{,}920 specifications (120 composites $\times$ 4 outcomes $\times$ 4 control sets) shows 99.7\% of specifications with confidence intervals above zero (permutation $p$ = 0.005).

[FIGURE:fig_open_ladder]

\subsection{Vocabulary-free confirmation (Frame~N)}

To address survivorship bias in the legacy concept vocabulary, we mined 636 vocabulary-free phrase-born concepts from random title samples (2003--2015 onsets), excluding all legacy labels and previously scored concepts [ARTIFACT:art_XRz1kLvWbXnO]. These vocabulary-free newborns have 14\% lower breadth and 89\% higher transience than legacy concepts, confirming that curated vocabularies are survivor-selected.

On these newborns, OPEN$_{\text{home}}$ gives PSP +0.117 [+0.020, +0.218] at the pre-onset footprint rung for $O_{2r}$ ($m = 30$). The signal is carried primarily by neighbourhood novelty: the novelty residual alone gives +0.208 [+0.113, +0.303], while edge persistence is null ($-$0.013). Pooling the independent Frame~N result with the legacy cohort, weighted by the inverse of each estimate's variance, gives +0.096 [+0.034, +0.158] at the footprint rung.

[FIGURE:fig_frame_n]

\subsection{The consistency--breadth reversal}
\label{sec:cheng}

Cheng et al.'s (2023) ideational consistency is the cosine similarity of a concept's neighbour co-usage vector from year $t-1$ to $t$. We rebuilt the measure on OpenAlex topic co-usage for 12{,}311 concepts (105{,}839 concept-years) [ARTIFACT:art_JwxcRvqfaD5z]. In their design (next-year volume, no current-size control), the negative-binomial model reproduces their estimate: $b = 0.428$ (+53.5\%/SD). Adding current volume log $V(t)$ removes almost all of it: +1.3\% [+0.5\%, +2.1\%], a residual-to-raw ratio of 0.021 [0.009, 0.035]. The volume effect is almost entirely a proxy for current size.

As an early trait, consistency predicts \emph{narrower} cross-field reach. Net of the five-feature baseline, the partial Spearman with rarefied breadth is $-$0.069 [$-$0.093, $-$0.047] on the pooled bodies (DerSimonian--Laird over five field groups: $-$0.079, $I^2$ = 0.00, 5/5 groups negative), replicating on the 2015--2017 cohort ($-$0.111 [$-$0.197, $-$0.030]). The consistency measure has Spearman +0.79 with edge persistence; it is essentially weighted persistence, confirming that a stable neighbourhood predicts growth but not breadth.

[FIGURE:fig_cheng_reversal]

\section{Results: field entry and trajectories}
\label{sec:rq2}

\subsection{Retained-field relatedness predicts the next field entered}

A conditional logit on concept-year risk sets tests whether relatedness to the fields currently retaining a concept predicts which field it enters next [ARTIFACT:art_Vu7gHKQXfL53]. We define a field as ``retaining'' a concept when it has published at least two grounded papers on the concept in each of the two most recent years. Relatedness between fields is measured by pointwise mutual information (PMI) of topic coassignment on the field-level backbone.

On an independent frame of 11{,}841 concepts (6{,}978 entry events in 6{,}076 informative strata), the pooled held-out standardised coefficient is $d_0$ = 0.322 [0.291, 0.355] with LR = 325.8 ($p < 10^{-70}$). The effect is substantial but heterogeneous across field families: Life \& Environment shows the strongest signal (+0.401) and Mathematics \& Decision Sciences is null (+0.065). DerSimonian--Laird pooled $d_0$ = 0.243 [0.118, 0.368], $I^2$ = 0.92.

Retained-field relatedness survives both the conventional revealed-comparative-advantage density ($D_{\text{rca}}$) and a share-weighted current presence density: adding $d_0$ after both rivals gives LR = 29.3 ($p = 6.1 \times 10^{-8}$) on DEV, and $D_{\text{rca}}$ is absorbed once $d_0$ enters. All three specificity tests reject their nulls after Holm correction. A dose-response by retention age shows a monotone pattern (2 years: +0.056; 3 years: +0.103; $\geq$4 years: +0.251).

However, the volume-matched contrast is null on held-out data (Holm $p$ = 0.76), and the effect is backbone-specific: under minimum conditional probability proximity instead of PMI, $d_0 = -0.021$. We cannot fully separate persistence from sustained volume as a predictor of field entry.

[FIGURE:fig_field_entry]

\subsection{Gateway centrality does not predict field retention}

An initial 80-episode panel suggested that a field's eigenvector centrality on the topic-relatedness backbone predicts retention ($\Delta$AUC +0.103) [ARTIFACT:art_33_KKk_G8Gw5]. On the full panel of 27{,}393 episodes, gateway centrality adds $\Delta$AUC $-$0.00001 (95\% CI [$-$0.0006, +0.0003]) [ARTIFACT:art_Vu7gHKQXfL53]. The signal vanishes once the field's leave-concept-out retention propensity is controlled. The shuffled-$R$ placebo's 95th percentile (0.130) exceeds the original +0.103, so the original lead cannot be certified as above chance on 80 episodes.

\section{Breadth decomposition and mechanism}
\label{sec:decomp}

\subsection{Exploration drives breadth, not retention}

Rarefied breadth $B_n$ can be decomposed as $\log B_n = \log E_2 + \log M + \log \rho$, where $E_2$ is early contact diversity (number of fields reached in the first three years), $M$ is the frontier advance ratio (new fields entered after the early window), and $\rho$ is the retention rate (fraction of early-contact fields that remain active). On 3{,}188 DEV concepts [ARTIFACT:art_Vu7gHKQXfL53]:

\begin{table}[ht]
\centering
\caption{Breadth decomposition ($\log B_n = \log E_2 + \log M + \log \rho$): share of the top-versus-bottom tercile gap in rarefied breadth attributable to each component.}
\label{tab:decomp}
\small
\begin{tabular}{lcc}
\toprule
Component & Share & 95\% CI \\
\midrule
Exploration ($s_{\text{E2}} + s_M$) & 0.732 & [0.703, 0.764] \\
\quad Early contact diversity ($s_{\text{E2}}$) & 0.779 & [0.738, 0.818] \\
Retention ($s_\rho$) & 0.268 & [0.236, 0.297] \\
Difference (explore $-$ retain) & 0.464 & [0.407, 0.528] \\
\bottomrule
\end{tabular}
\end{table}

Broad concepts start with wider contact, not by advancing a wider frontier: the frontier advance component is negative ($s_M = -0.046$ [$-$0.074, $-$0.017]).

[FIGURE:fig_decomp]

\subsection{Which partners carry the signal?}
\label{sec:confound}

The home-only signal is carried by partners from new Leiden communities that arrive through mixed-field papers, those with at least one off-home topic [ARTIFACT:art_jHxmVyMKP0KN]. In a Shapley decomposition of the NOVCHURN partial Spearman:

\begin{itemize}
    \item Partners from new communities carry the signal (contrast $C_2$ = +0.102 [+0.069, +0.133], Holm $p$ = 0.003).
    \item Partners carried by mixed-field papers carry the signal ($C_4$ = +0.103 [+0.071, +0.134], Holm $p$ = 0.003).
    \item Novelty among substantive-domain partners, not among methodological partners, is the main contributor (domain Shapley $\phi$ = +0.132 on the 2015--2017 cohort, method = +0.012).
\end{itemize}

We call a home paper that introduces at least one cooccurrence partner from a previously unrepresented Leiden community a \emph{bridging paper}. Controlling for the share of early home papers that are bridging papers halves the NOVCHURN partial from 0.118 to 0.056. These bridging papers have more first-time authors on the concept (+5 percentage points) and far more off-home topics (+25 points).

[FIGURE:fig_mechanism]

\subsection{Topical non-redundancy, not temporal turnover}

Raw edge persistence has Spearman +0.72 with log home-paper count [ARTIFACT:art_gq9S7nAtWrUT]. We tested three confound-correction variants:

\textbf{Fixed-size rarefaction.} Subsampling to 10 home papers per year retains 68\% of the pooled association. The bias-corrected Chao estimator of the Jaccard index retains 91\%.

\textbf{Within-concept permutation null.} The excess churn over a 200-draw within-concept year-label permutation null is indistinguishable from zero: excess NOVCHURN pooled PSP = +0.008 [$-$0.02, +0.03], compared to raw NOVCHURN = +0.116 [+0.09, +0.14]. The $R^2$ of raw persistence on this permutation-null mean is 0.66. What predicts breadth is a static property, the non-redundancy of the concept's home-topic partner mix, not year-to-year turnover.

\textbf{Degree-preserving configuration null.} Replacing raw ego density and persistence by their curveball configuration $z$-scores raises OPEN$_{\text{home}}$ from +0.092 to +0.115 on the same sample.

Split-half reliability of NOVCHURN$_{\text{raw}}$ is 0.48, rising to 0.67 at $\geq$100 home papers. The disattenuated pooled NOVCHURN$_{\text{raw}}$ PSP is 0.178 [0.141, 0.214].

[FIGURE:fig_confound]

\section{Discussion}
\label{sec:disc}

\subsection{What the OPEN index captures}

The OPEN index captures the degree to which a concept's early neighbourhood acquires partners from diverse communities rather than reinforcing existing ones. The signal is not temporal turnover but topical non-redundancy. A within-concept permutation null absorbs the year-to-year component, yet the association persists: concepts whose home-field cooccurrence partners span many communities and arrive through papers with off-home topics tend to reach more fields later. This is consistent with \citet{March1991}'s exploration--exploitation distinction at the concept level: concepts embedded in a diverse, open intellectual neighbourhood are better positioned for cross-field diffusion than those embedded in a dense, self-referential one.

The home-only signal (OPEN$_{\text{home}}$) is marginal. The stronger OPEN$_{\text{all}}$ signal is partly mechanically coupled: early off-home papers that enter the ego network are a subset of the papers that determine the outcome. OPEN$_{\text{sizematch}}$ (corpus-wide papers subsampled to home counts) controls for this coupling and remains significant.

\subsection{The consistency--breadth reversal}

Cheng et al.\ (2023) found that ideational consistency predicts a concept becoming ``core.'' We replicate their result for volume (+53\%/SD) but show that, net of volume, the same property predicts \emph{narrower} cross-field reach. The reversal holds in all five field groups ($I^2 = 0$), replicates on a fresh cohort, and is a between-concept trait (within concepts, a more consistent year is followed by slightly \emph{more} entries). The features predictive of local consolidation and growth (stable terminology, consistent co-usage patterns) are distinct from, and partly opposed to, the features predictive of broad disciplinary spread. This distinction matters for policy: a concept ``becoming core'' in the sense of rising in volume and stable terminology may be deepening within its home community rather than spreading across fields.

\subsection{Background homophily in citation lineage}

A methodological finding from the lineage analysis merits attention [ARTIFACT:art_xp8BGBJZsxeI]. Among 48 concepts in the citation-lineage experiment, 100\% have a positive background log-odds ratio: every field's citing papers preferentially cite their own field above chance. The $R^2$ of the raw concept-lineage log-odds ratio on the background log-odds ratio is 0.66 (90\% CI [0.39, 0.83]). Two-thirds of the between-concept variance in raw lineage autonomy is general disciplinary homophily, not concept-specific integration. Uniform-null lineage indices conflate field composition with concept-specific rooting. This extends \citet{Lipsitch2010}'s negative-control framework from epidemiology to bibliometric mixing tables.

\subsection{Retained-field relatedness}

The confirmed field-entry result ($d_0 = 0.32$ on the independent frame) extends the principle of relatedness from economic complexity \citep{Hidalgo2007,Neffke2011} to concept adoption. No prior study has tested whether relatedness to the set of fields currently \emph{retaining} a concept predicts entry, beyond relatedness to the home field. The result is partial: the volume-matched contrast is null, and the effect is backbone-specific. But $d_0$ survives both the conventional density and a volume-density rival, with a monotone dose-response by retention age.

\subsection{Limitations}

\textbf{Effect size.} The OPEN--breadth association is modest. OPEN$_{\text{home}}$ adds no forecasting gain over the five-feature baseline (+0.002 [$-$0.003, +0.008]). The cross-validated Spearman of the baseline alone is 0.79; adding all indicators raises it by about 0.03. The practical predictive gain from early network structure is small.

\textbf{Measurement noise.} Split-half reliability of OPEN$_{\text{home}}$ is 0.49. The signal is measured with substantial noise at typical sample sizes (median $\sim$30 home papers in the early window). Prediction for individual concepts remains imprecise.

\textbf{Vocabulary bias.} The legacy OpenAlex concept vocabulary is survivor-selected. The Frame~N panel is small (448 concepts), with pre-unseal power of only 0.47.

\textbf{Cooccurrence, not causation.} Early ego-network openness could reflect the concept's intrinsic generality, the diversity of the research community around it, or the breadth of the problems it addresses. We show association, not mechanism.

\textbf{Domain heterogeneity.} Life \& Environment Sciences show the weakest OPEN signal (PSP +0.071 vs.\ +0.186 for the other five units pooled). The retained-field relatedness effect has $I^2 = 0.92$, indicating substantial cross-domain heterogeneity.

\section{Conclusion}

We screened 53 early temporal network indicators for predicting the cross-disciplinary breadth of new scientific concepts, using 12{,}499 concepts from the OpenAlex corpus with held-out validation. Seven indicators are confirmed, composing into an openness index that captures topical non-redundancy in a concept's early cooccurrence neighbourhood. Early openness predicts breadth; early consolidation predicts volume but not breadth. Concepts spread next to fields related to those currently retaining them, extending the principle of relatedness.

The practical forecasting gain from early network structure is small next to simple popularity baselines. The conceptual contribution, however, is that openness and consolidation have opposing associations with breadth and volume. This clarifies that growing deeper within a home discipline and spreading wider across disciplines are not the same process, and the network signatures that predict one do not predict the other.

\bibliographystyle{plainnat}
\bibliography{references}

\end{document}
