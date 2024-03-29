# AI Studio Project

## Overview

This project focuses on developing a machine learning model to classify entities within a dataset of 10,000 entries, distinguishing between individuals and companies. Tailored for third-party companies with extensive client bases, the project strategically employs web scraping techniques to enhance data collection and model training. It usees Python and popular libraries such as TensorFlow and scikit-learn.

### Key Achievements

- Achieved outstanding metrics (precision, recall, and F1 score consistently above 90%) for entity classification across diverse languages (English, Chinese, Arabic, etc.).
- The incorporation of web scraping enriches the dataset, contributing to the model's robustness.
- Practical application aids organizations in swiftly discerning client types, optimizing service delivery for improved client satisfaction.


## Model Evaluation

| Model Name            | Description                                                                                                       | Results                                                   | Pros                                              | Cons                                       |
|-----------------------|-------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|---------------------------------------------------|--------------------------------------------|
| K-Nearest Neighbors   | Uses proximity to make classifications or predictions about the grouping of an individual data point              | AUC = 92.8%, Precision = 83.8%, Recall = 94.6%, F1 Score = 88.9% | Simple, constantly evolves                    | Can be slow with large datasets, sensitive to dimensionality |
| Logistic Regression    | Uses a sigmoid function to return the probability of a label                                                      | AUC = 89%, Precision = 79%, Recall = 91.6%, F1 Score = 84.8%   | Easy to implement, easy to update                | Sensitive to outliers, prone to overfitting  |
| Gradient Boosted Descent | Trains simple models on the errors of previous models, each new model focuses on the weaknesses of the previous iteration | AUC = 97%, Precision = 91%, Recall = 85%, F1 Score = 88% | No data preprocessing, flexible               | Less interpretable, may lead to overfitting, requires significant space and time |
| Random Forest          | Generates a group of decision trees and takes the majority vote to classify information                           | AUC = 96%, Precision = 89%, Recall = 83%, F1 Score = 86%  | Does not tend to overfit, adapts well to more features | Less interpretable, slow with large datasets |


## Model Selection

After evaluating various models, we have decided to choose the **K Nearest Neighbors (KNN) Model** for our project. The decision is based on its higher F1 and recall scores, indicating strong performance in entity classification.

## Runner Up

The **Gradient Boosted Descent Model** emerges as our runner-up. Despite not being the primary selection, it showcases a high level of precision. Additionally, its F1 score is within 0.9 of the KNN model, making it a noteworthy alternative.

## Feature Engineering Highlights (8 new features) 

#### Language Detector:

Language detection enhances adaptability across multiple languages using the "alphabet-detector" Python package.

```python

import subprocess
import sys

def ad_col():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "alphabet-detector"])
    from alphabet_detector import AlphabetDetector
    ad = AlphabetDetector()
    df['langs_ad'] = df['Entity Name'].apply(lambda x: [ad.detect_alphabet(x)])
    df['langs_ad'] = df['langs_ad'].str[0]
    df['langs_ad'] = [list(e) for e in df.langs_ad]
    df['langs_ad'] = df['langs_ad'].str[0]

```

#### Word Length Feature:

Captures word length, aiding in discerning patterns indicative of entity type.

#### Punctuation Feature:

Analyzes and leverages punctuation marks, enhancing entity classification accuracy.

#### Contains Number Feature:

Identifies the presence of numbers within entities, aiding in distinguishing between individual and company names.

#### Contains Company Suffix or Prefix Feature:

Detects common company suffixes or prefixes, contributing to precision in identifying entities as companies.

#### Conjunction/Stopword Feature:

Focuses on conjunctions and stopwords, refining the model's understanding of language structures.

#### Contains Location Name Feature:

Identifies location names within entities, enhancing contextual understanding.

#### Contains Common Person Name Feature:

Recognizes common person names, contributing to accurate identification of entities as individuals.
