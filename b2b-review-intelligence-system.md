# B2B Manufacturing Review Intelligence System

**A Narrow AI System for Sentiment Classification and Image-Based Review Verification**

---

## 1. Overview

| | |
|---|---|
| **Project Title** | B2B Manufacturing Review Intelligence System |
| **Use Case Type** | Classification + Image Verification (Narrow AI) |
| **Domain** | B2B Manufacturing — Rigid Plastic & Glass Packaging |
| **Status** | Problem Definition & Evaluation Plan |

---

## 2. User & Practical Problem

### 2.1 The User

The primary user is the **Owner of a B2B manufacturing firm** that produces PET bottles, double-wall jars, and pharmaceutical and skincare packaging. The owner manages the business end-to-end and is directly responsible for:

- Order intake and client communication
- Custom product design requests
- Raw material stock management

### 2.2 The Problem

Because the owner personally handles daily operations, there is no time to manually read through the growing volume of B2B client reviews arriving across **IndiaMART, Alibaba, and Amazon Business**. With **10,000+ order records** accumulated, the business currently has:

- **No visibility** into overall client satisfaction (what percentage of clients are actually happy vs. dissatisfied).
- **No systematic way to prioritize** which negative reviews need urgent attention.
- **No mechanism to verify authenticity** of complaint photos — when a client attaches a photo to a negative review, there is currently no way to confirm whether the defective product shown is genuinely the firm's own bottle/jar or a photo of a competitor's product being used to file a false or exaggerated claim.

This last issue is the highest-impact pain point: unverified negative reviews with mismatched photos can unfairly damage the firm's reputation on B2B marketplaces, while genuine defects may go unaddressed if lost in the noise.

### 2.3 Why This Is a Good Narrow AI Fit

Both sub-problems are well-scoped, well-bounded classification tasks rather than open-ended reasoning problems:

1. **Text sentiment classification** — a 3-class problem (Positive / Negative / Neutral) over short review text.
2. **Image similarity verification** — a binary comparison task (does the client photo match the firm's own product catalog?) rather than open-domain image recognition.

Neither task requires large-scale infrastructure, making this feasible to deploy on the owner's existing hardware.

---

## 3. Data Source

| Attribute | Detail |
|---|---|
| **Dataset Name** | `manufacturing_b2b_dataset.xlsx` (Sheet: *Orders & Reviews*) |
| **Size** | 10,000 rows × 25 columns |
| **Key Columns Used** | `Client Review` (text), `Review Sentiment`, `Review Rating (1–5)`, `Photo Provided After Delivery` (Yes/No), `Photo File Reference`, `Product Name` (PET Jars, Caps, Pumps, Double Wall Jars, Glass Jars, Foaming Bottles, Serum Bottles, Pharmaceutical Range) |
| **Document / Sheet Link** | *[Insert Google Sheet / shared drive link here before submission]* |

### 3.1 Class Distribution

| Sentiment | Count | Share |
|---|---|---|
| Positive | 5,476 | 54.7% |
| Negative | 2,956 | 29.5% |
| Neutral | 1,568 | 15.6% |
| **Total** | **10,000** | **100%** |

Of the total orders, **3,220 reviews include a client-uploaded photo**, which forms the candidate pool for the image verification module (Part B).

---

## 4. Constraints

| # | Constraint | Implication for Design |
|---|---|---|
| a | **Limited data volume.** This is a B2B dataset (10,000 records), not a B2C-scale dataset with millions of reviews. | Favor lightweight, sample-efficient models (e.g., TF-IDF + Logistic Regression, or a fine-tuned DistilBERT) over models that require massive labeled corpora. |
| b | **Mixed-language text (Hinglish).** Reviews naturally mix Hindi and English, e.g., *"cap loose hai, quality mast hai"*. | The text classifier must handle code-mixed language; multilingual/Hinglish-aware tokenization or embeddings are required rather than English-only models. |
| c | **Variable image quality.** Client-submitted photos (from the 3,220 available) may be low-light, blurry, or poorly framed. | The image verification model must be robust to real-world photo conditions, not just clean catalog images. |
| d | **Hardware limitations.** The system must run on the owner's standard business laptop — no dedicated GPU. | Prefer compact/distilled models and CPU-friendly inference (e.g., DistilBERT over full BERT; a lightweight CLIP variant with batched, on-demand inference rather than continuous GPU workloads). |
| e | **Data privacy.** Client firm names are commercially sensitive and must not be exposed or leaked in any output, report, or model artifact. | Client Firm Name and other identifying fields must be excluded from model training features and masked/anonymized in any shared dashboard or report. |

---

## 5. Proposed AI Workflow

### Part A — Text Classification (Sentiment Analysis)

**Input:** `Client Review` (free text, Hinglish/English mixed)
**Model options:** TF-IDF + Logistic Regression (baseline) → DistilBERT (fine-tuned, if higher accuracy is needed)
**Output:** Predicted class — Positive / Negative / Neutral — aggregated into a live percentage dashboard (e.g., *"75% Positive this month"*)

**Pipeline:**
1. Clean and normalize review text (handle Hinglish tokens, remove noise).
2. Vectorize (TF-IDF baseline) or tokenize (DistilBERT).
3. Classify into 3 sentiment classes.
4. Aggregate results into a rolling dashboard view (daily/weekly/monthly satisfaction %).

### Part B — Image Verification (Complaint Authenticity Check)

**Trigger condition:** `Review Sentiment = Negative` **AND** `Photo Provided = Yes`

**Model:** CLIP (or a lightweight CLIP variant) for image-to-image similarity

**Pipeline:**
1. Take the client-submitted photo attached to the negative review.
2. Compare it against the firm's own reference product catalog images (matched by `Product Name`, e.g., PET Jars reference set).
3. Compute similarity score.
4. Classify:
   - **Similarity ≥ 80%** → *Verified Complaint* (genuinely the firm's product — route to quality team)
   - **Similarity < 80%** → *Unverified / Possible Mismatch* (flag for manual review before any action is taken)

> **Note on fairness:** A low similarity score should be treated as *"needs manual review,"* not as automatic proof of a fake review — lighting, angle, and packaging changes over time can also lower similarity scores. The model assists prioritization; it does not make final accusations.

---

## 6. Evaluation Approach & Success Criteria

### 6.1 Text Classification (Part A)

| Metric | Target | Validation Method |
|---|---|---|
| F1-Score (macro, across 3 classes) | **> 0.85** | Held-out test split from the 10,000-row dataset |
| Accuracy | Reported alongside F1 | Same test split |
| Manual spot-check | 100 randomly sampled reviews | Human-reviewed against model predictions to catch Hinglish edge cases the metric may hide |

### 6.2 Image Verification (Part B)

| Metric | Target | Validation Method |
|---|---|---|
| Classification Accuracy | **> 80%** | Controlled test set: 20 genuine photos of the firm's own products + 20 photos of a different company's products |
| False Positive Rate (flagging genuine products as mismatched) | Tracked separately | Same 40-image test set |

### 6.3 Business Success Criteria

Beyond model metrics, the system is considered successful if it delivers measurable operational value:

- **Time savings:** The owner's manual review-reading time is reduced by an estimated **60 minutes/day**.
- **Faster root-cause response:** Root cause of a negative review (defect, delivery damage, or possible fake claim) is identified within **24 hours**, instead of remaining unnoticed indefinitely.
- **Reputation protection:** Reduction in unresolved/unverified negative reviews sitting unaddressed on public B2B marketplaces.

---

## 7. Known Limitations & Future Scope

- The 10,000-row dataset, while sufficient for a functional first version, is modest relative to B2C-scale systems — model performance should be re-validated as more labeled data accumulates.
- Hinglish coverage will improve over time as more real client language patterns are incorporated into training data.
- Future iterations could extend the image model to detect *specific defect types* (cracks, cap misalignment, discoloration) rather than only verifying product identity.

---

## 8. Conclusion

This system directly targets the two highest-friction problems in the owner's daily workflow — **information overload from unread reviews** and **inability to verify complaint authenticity** — using two narrow, well-bounded AI components that are realistic to build and deploy on standard business hardware, without requiring the owner to change how they currently collect reviews across IndiaMART, Alibaba, and Amazon Business.
