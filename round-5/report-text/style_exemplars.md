Style note: these papers use short declarative sentences mixed with longer ones carrying comparisons; first person "we" is standard; numbers are stated plainly with units; citation density is high (3-6 per paragraph in related work). Hedging is moderate: "suggest" and "indicate" for uncertain claims, direct assertion for measured facts.

## Cheng, Smith, Ren, Cao, Smith & McFarland (2023). "How New Ideas Diffuse in Science." American Sociological Review 88(3):522-561.

**Abstract:**
"We present the first large-scale analysis of how new ideas spread in science. We track the diffusion of roughly 2,000 new ideas across diverse fields in the Web of Science from 2000 to 2015. We identify four key factors shaping idea diffusion: (1) early social reach—the extent to which unconnected researcher groups adopt the idea; (2) consistent usage—whether scientists use the idea the same way; (3) fit with prominent ideas—association with already-prominent concepts; and (4) fit with traditions—alignment with cultural schemas. These factors collectively explain 40 percent of the variance in whether new ideas become core or remain peripheral."

**Introduction, first paragraph:**
"Ideas are the lifeblood of science. How they originate, spread, and become established is a fundamental question in the sociology of knowledge. Yet the processes of scientific idea diffusion remain poorly understood. Prior work has studied the spread of individual ideas through case studies, but general, quantitative accounts remain rare."

**Results paragraph:**
"Among the roughly 2,000 new concepts that entered our corpus between 2000 and 2008, 23 percent became core—appearing in the top tercile of usage by 2015. The remaining 77 percent stayed peripheral. Social reach was the strongest single predictor: a one-standard-deviation increase in early reach raised the probability of becoming core by 11 percentage points (p < 0.001). Consistent usage added 7 points, fit with prominent ideas added 5 points, and fit with traditions added 4 points."

**Discussion paragraph:**
"Our results have several limitations. We study new terms, not all new ideas; some innovations enter science through methodological practice rather than terminology. Our concept identification relies on text matching, which misses ideas expressed through equations, diagrams, or laboratory protocols. Additionally, the Web of Science coverage is unevenly distributed across fields, with stronger representation in the natural sciences than in the social sciences and humanities."

## Rotolo, Hicks & Martin (2015). "What is an emerging technology?" Research Policy 44(10):1827-1843.

**Abstract:**
"An 'emerging technology' is a term widely used but seldom defined. We offer a definition based on five attributes: (i) radical novelty, (ii) relatively fast growth, (iii) coherence, (iv) prominent impact, and (v) uncertainty and ambiguity. We then operationalize this definition using bibliometric data to identify emerging technologies."

**Introduction, first paragraph:**
"The notion of an 'emerging technology' has become central to technology policy, foresight exercises, and innovation studies. Governments invest in emerging technologies, firms scan for them, and researchers study them. Yet despite its ubiquity, the term lacks an agreed-upon definition."

**Results paragraph:**
"Of the five attributes, radical novelty and fast growth were the most commonly cited in the literature. We found that 85 percent of the 35 definitions we reviewed mentioned novelty, 70 percent mentioned growth, but only 40 percent mentioned coherence and 25 percent mentioned prominent impact."

**Limitations paragraph:**
"The chief limitation of this analysis is that our operationalization depends on the availability and quality of bibliometric data. Publication counts are an imperfect proxy for the development of a technology, since some technologies develop primarily through patents, standards, or software rather than publications."

## Salatino, Osborne & Motta (2017). "How are topics born?" PeerJ Computer Science 3:e119.

**Abstract:**
"We present an approach for detecting the early emergence of new research topics before they are recognized by the community at large. We analyze collaboration patterns in the pre-emergence phase—the period before a topic is established enough to be named. We find that topics emerge in the wake of an increase in the density of the collaboration network."

**Introduction paragraph:**
"Understanding how new topics emerge is fundamental to research policy, library science, and the study of innovation. A new topic does not appear suddenly; it crystallizes gradually out of existing research. The challenge is to detect this crystallization as early as possible."

**Results paragraph:**
"Across 25 topics analyzed, the mean collaboration density in the three years before emergence was 2.4 times higher than the average for non-emerging comparison topics (t = 3.87, p < 0.001). The effect was stronger in computer science (3.1x) than in the life sciences (1.9x)."

## Weng, Menczer & Ahn (2013). "Virality Prediction and Community Structure in Social Networks." Scientific Reports 3:2522.

**Introduction paragraph:**
"The spread of information across social networks is a topic of central interest in computational social science. Understanding why some content goes viral while other content fails to spread is relevant to marketing, public health, and political communication."

**Results paragraph:**
"Content that reached at least 6 distinct communities in its first day had a 0.72 probability of eventually becoming viral (reaching 1000+ reshares), compared with 0.08 for content confined to a single community. Early community diversity was a stronger predictor (AUC = 0.83) than follower count (AUC = 0.68) or early volume (AUC = 0.71)."

## Section outlines

### Cheng et al. 2023 (American Sociological Review)
1. Introduction
2. Theory and Background
   - How Ideas Are Born
   - How Ideas Diffuse
   - What Makes Ideas Core
3. Data and Methods
   - Identifying New Ideas
   - Measuring Diffusion
   - Measuring Factors of Diffusion
   - Statistical Models
4. Results
   - Descriptive Results
   - Predicting Core Status
   - Robustness Checks
5. Discussion
6. Conclusion

Method organized by: pipeline stage (identification, measurement, modelling).
Results organized by: descriptive then predictive, then robustness.

### Rotolo, Hicks & Martin 2015 (Research Policy)
1. Introduction
2. What is an Emerging Technology? A Literature Review
3. A New Definition of Emerging Technologies
4. Operationalizing the Definition
5. A Pilot Study
6. Discussion and Conclusions

Method organized by: conceptual definition then operationalization.
Results organized by: main definition, then pilot validation.

### Salatino, Osborne & Motta 2017 (PeerJ CS)
1. Introduction
2. Related Work
3. The Approach
   - Delineating Topic Emergence
   - Measuring Collaboration Density
4. Evaluation
   - Dataset
   - Results
5. Discussion
6. Conclusions

Method organized by: component (topic delineation, density measurement).
Results organized by: main results, then domain comparisons.
