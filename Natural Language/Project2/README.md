# LN_MP2

**Running Command**  
```python qc.py -test dev.txt -train trainWithoutDev.txt```

# RESULTS
| Model | Correct Answers (%) |
|:-----:|:-------------------:|
| Baseline (Random) | 19.72% |
| Compare nouns and verbs | 71.4% |
| TF-IDF | 77.6% (388/500) |
| ComplementNB com Lower Case | 89.4% (447/500) |
| ComplementNB sem Lower Case | 89.2% (446/500) |
| ComplementNB with Stop words | 88.8% (444/500) |

# Rules
Mr. Mrs. Ms. - remove the space after
