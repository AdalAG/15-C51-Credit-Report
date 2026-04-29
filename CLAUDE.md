# Project 2: Credit Approval Rule Analysis

## Goal
Understand the rules behind credit approval decisions — not to maximize OOS prediction, but to identify which features drive decisions, in what direction, and how they interact. Interpretability is the primary objective.

## Data
- Source: UCI Credit Approval dataset (`credit_approval/crx.data`)
- 690 rows × 16 columns (A1–A15 features, A16 class label +/-)
- All feature names and values are anonymized symbols; meaning is unknown
- Parsed to `credit_approval/credit_approval.csv` (with header row)
- Missing values (~37 rows, ~5%): **drop, do not impute** — imputation assumptions are unjustifiable when feature meanings are unknown

## Pipeline

### 1. Preprocessing
- Drop rows with missing values (~37 rows → ~653 remaining)
- No test set — all data used for CV; generalization is not the goal

### 2. Model Selection via K-Fold CV (K=10)
- Use `RandomizedSearchCV` to tune Random Forest, optimizing mean AUC
- **Stability-first selection**: among models where mean CV AUC exceeds a reasonable floor (e.g., 0.80), choose the one with the lowest std(AUC) across folds
- Rationale: a stable model produces more trustworthy importance estimates for interpretation; a model that wildly changes across folds is not reliable as a lens into the data

### 3. Feature Importance (across folds)
- Use **permutation importance** or **SHAP values** — not MDI (`feature_importances_`)
  - MDI is biased toward high-cardinality continuous features; this dataset has several (A2, A3, A8, A14, A15)
- Compute importance **within each fold** and report mean ± std across folds
- Features that are consistently important across folds are trustworthy for interpretation; high-variance importance signals an artifact

### 4. Feature Analysis (top features)
For each top feature (and key pairs):

| Analysis | Tool | What it reveals |
|---|---|---|
| Importance stability | Bar chart with error bars (across folds) | Which features are robustly important |
| Feature correlations | Heatmap of top features | Collinear features split importance; interpret jointly |
| Conditional distributions | KDE (continuous) / bar (categorical) by outcome | Model-free sanity check; should align with importance |
| Direction & monotonicity | PDP + SHAP main effect plots | Sign and shape of each feature's effect |
| Heterogeneity | ICE plots | Whether the effect is uniform or varies across individuals |
| Interactions | 2-way PDP, SHAP interaction values, SHAP dependence colored by second feature | Which feature pairs jointly influence decisions |
| Borderline cases | SHAP waterfall plots (P ≈ 0.45–0.55) | Model logic at the margin, where decisions are consequential |
| Sign sanity check | Regularized logistic regression (L1/L2) | Agreement with RF → pattern is in the data; disagreement → investigate |
| Direction stability | SHAP sign per fold | A feature whose direction flips across folds is unreliable |

## Key Rationale
- **No test set**: justified because the goal is understanding the data-generating process, not estimating generalization error
- **Stability over raw performance**: a model that generalizes consistently across folds is more interpretable than one with higher mean AUC but high variance
- **Permutation/SHAP over MDI**: avoids cardinality bias in importance ranking
- **Logistic regression as cross-check**: if RF and LR agree on top features and directions, the finding is more credible; disagreement may indicate nonlinearity or collinearity artifacts
- **ICE over PDP alone**: PDP averages can mask heterogeneous effects; ICE reveals whether a feature's effect is consistent across individuals
