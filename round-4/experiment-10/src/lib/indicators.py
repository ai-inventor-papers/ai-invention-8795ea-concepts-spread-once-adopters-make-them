"""The RQ1 indicator dictionary: name -> (family, formula). Window t0..t0+2 for every indicator."""
from __future__ import annotations

B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]

FAMILIES: dict[str, list[tuple[str, str]]] = {
    "E": [("share", "grounded works t0..t0+2 per million base works (EXP5)"),
          ("growth_ind", "log((N_t0+2 + 1)/(N_t0+1 + 1)) (EXP5)"),
          ("accel", "quadratic coefficient of log1p(N) over t0..t0+2 (EXP5)"),
          ("burst", "Kleinberg 2-state burst weight t0-3..t0+2 (EXP5)"),
          ("author_growth", "log1p(distinct authors t0+2) - log1p(distinct authors t0) (Pass A)"),
          ("n_authors_early", "log1p(distinct authors t0..t0+2) (Pass A)")],
    "F": [("log_offhome_volume", "log1p(off-home venue-labelled works t0..t0+2) (EXP5)"),
          ("rao_stirling", "sum_ij p_i p_j (1 - phi_ij/max phi), venue-field shares t0..t0+2, EXP6 1998-2002 PMI phi"),
          ("fields_gained_per_yr", "(|ENTERED(t0+2)| - |ENTERED(t0)|)/2, off-home, counts restricted to t0..t0+2")],
    "G": [("G", "gateway(eig)-weighted off-home landing (EXP5; previously scored on held-out)"),
          ("G_A", "G over t0..t0+1 (EXP5; previously scored)"),
          ("G_btw", "betweenness-gateway landing (EXP5; previously scored)"),
          ("G_deg", "degree-gateway landing (EXP5)"),
          ("G_phimin", "phi_min-gateway landing (EXP5)"),
          ("REL_home", "mean phi(home, landing field) of off-home works (EXP5)"),
          ("RS", "Rao-Stirling with 1 - phi_min distances (art_33 / EXP5)")],
    "FR": [("CONTACT_REACH", "# off-home fields with >= 1 labelled work t0..t0+2"),
           ("RETAINED_REACH", "# off-home fields with >= 2 works in >= 2 of the 3 years"),
           ("RETENTION_RATIO_early", "RETAINED_REACH / max(CONTACT_REACH, 1)"),
           ("FRONTIER_POTENTIAL", "sum_{k not entered, off-home} mean_{j retained} phi[j,k]"),
           ("D_rca_end", "# off-home fields entered by the RCA rule by t0+2 (EXP6 h2.rca_entered)"),
           ("D_vol_end", "# off-home fields with cumulative >= 2 works by t0+2 (EXP6 h2.states)"),
           ("M0_density_end", "mean Hidalgo density phi[E].sum/colsum over not-entered off-home fields at t0+2")],
    "A": [("D_z", "z of # backbone communities reached by NEW neighbours vs frequency-matched null (200 draws)"),
          ("D_ratio", "observed / null-mean # communities of NEW neighbours"),
          ("D_rare", "rarefied (r=10) # communities of NEW neighbours"),
          ("D_sub", "z of # subfields reached by NEW neighbours"),
          ("D_obs", "# distinct communities of NEW neighbours"),
          ("NOV", "share of NEW neighbours outside the W1 dominant community"),
          ("NOV_res", "NOV minus its degree-preserving expectation"),
          ("F_res", "growth of mean top-20 neighbour PMI W1->W3 minus multinomial-null mean"),
          ("F_z", "F_res / null SD"),
          ("deg_W1", "# PMI>0 neighbours (n>=2) in W1 = t0"),
          ("deg_W3", "# PMI>0 neighbours in W3 = t0+2"),
          ("deg_growth", "log(deg_W3+1) - log(deg_W1+1)"),
          ("str_growth", "log(sum PMI W3 + 1) - log(sum PMI W1 + 1)"),
          ("new_edge_rate", "(M/3) / (deg_W1 + 1)"),
          ("edge_persistence", "mean Jaccard of neighbour sets W1-W2, W2-W3"),
          ("turnover", "share of W1 neighbours absent in W3"),
          ("participation", "1 - sum of squared community shares of W3 neighbours"),
          ("n_comm_W3", "# communities among W3 neighbours"),
          ("comm_entropy", "Shannon entropy of W3 neighbour community weights"),
          ("comm_transitions", "# changes of dominant community W1->W2->W3"),
          ("ego_density_W3", "backbone edge density among W3 neighbours"),
          ("ego_density_change", "ego density W3 - W1"),
          ("btw_end", "betweenness (cutoff 3) of the concept inserted in the kNN backbone at t0+2"),
          ("btw_change", "btw_end - btw at t0"),
          ("kcore_end", "k-core number of the inserted concept at t0+2"),
          ("constraint_end", "Burt constraint of the inserted concept at t0+2"),
          ("constraint_change", "constraint t0+2 - t0")],
    "S": [("S_comp", "# co-author components / # off-home early works (with author ids)"),
          ("S_comp_n", "# co-author components / # distinct off-home authors"),
          ("S_isolated_share", "share of off-home early works sharing no author with another off-home work")],
}

INDICATORS = [n for fam in FAMILIES.values() for n, _ in fam]
FAMILY_OF = {n: f for f, lst in FAMILIES.items() for n, _ in lst}
FORMULA_OF = {n: t for lst in FAMILIES.values() for n, t in lst}
PREVIOUSLY_SCORED = {"G", "G_A", "G_btw"}

CONT_OUTCOMES = ["O1c", "O2r_m50", "O2r_resid", "O4"]
BIN_OUTCOMES = ["O1b", "O3", "O5", "O5_WW"]
OUTCOMES = CONT_OUTCOMES + BIN_OUTCOMES
T0_BASELINE_OUTCOMES = {"O5", "O5_WW"}      # B5 + onset-year dummies (Wikipedia creation wave)

PREREG = {
    "P1": "entropy, D_rare, D_ratio, participation, NOV_res: raw Spearman with O2r_m50 > 0 (CI > 0) in >= 3 of 4 held-out "
          "groups; AND D_rare, D_ratio, participation, NOV_res: pooled psp|B5 CI upper bound < 0.10",
    "P2": "edge_persistence: pooled raw rho and pooled psp with O2r_m50 both < 0",
    "P3": "deg_growth, str_growth, new_edge_rate FAIL held-out: pooled psp CI includes 0 OR sign flip in >= 2 of 4 groups",
    "P4": "RETENTION_RATIO_early and FRONTIER_POTENTIAL: pooled psp > 0 with CI > 0 for O2r_resid AND O1c",
    "P5": "CONTACT_REACH: pooled psp CI includes 0 (also reported given B5 minus reach)",
}
PREREG_INDICATORS = {"entropy", "D_rare", "D_ratio", "participation", "NOV_res", "edge_persistence", "deg_growth",
                     "str_growth", "new_edge_rate", "RETENTION_RATIO_early", "FRONTIER_POTENTIAL", "CONTACT_REACH"}
