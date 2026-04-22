# A/B-test Visibility Boost based on Thailand OTA Market Equilibrium and Drift

## 1. Context and Problem

Thailand OTA market dynamics across main cities *(Bangkok, Chiang Mai, Krabi, Pattaya and Phuket)* were analyzed using the [Market Equilibrium and Drift (MED)](https://github.com/SuslovAnton/ota-market-equilibrium-and-drift) framework.   
Results show that **Phuket** and **Krabi** are currently in a `PRICE_WAR` macro phase. However, RevPAR decline decomposition reveals that the drop is primarily `OCC_LED` (occupancy led) with ~90% occupancy contribution. That points towards `DEMAND_CRISIS` decline profile and a **demand-side problem** rather than pricing fault.    

Therefore, an A/B-test was designed to evaluate if increasing property visibility can improve **Conversion Rates (CR)** in Phuket and Krabi markets, dragging **Occupancy** and **RevPAR** higher.


## 2. Experiment Design Outlines

### Unit of Randomization

Users are **randomly assigned** to control and treatment groups (in 50/50 proportion):
- **Control:** standard ranking (NO visibility boost).
- **Treatment:** boosted visibility for selected properties.

> **Note:** Results are evaluated at the city level (Phuket, Krabi) to mitigate marketplace effect (interference).  

### Hypothesis

- **$H_0$ (Null Hypothesis):**   
The visibility boost has **no effect** on Conversion Rate (CR).   
`CR_treatment = CR_control`   
   
- **$H_1$ (Alternative Hypothesis):**   
The visibility boost **increases** Conversion Rate (CR).   
`CR_treatment > CR_control`

### Metrics

- **Primary Metric:**
    - **Conversion Rate (CR):** share of users who complete a booking (bookings / sessions).
- **Secondary Metric:**
    - **RevPAR:** to evaluate revenue impact.
- **Guardrail Metrics:**:
    - **ADR:** ensure there's no significant transition of demand from more expensive options.
    - **Cancellation Rate:** ensure booking quality is not harmed.   

### Significance Level and Power

The next statistical design has been chosen for the test:
- **Significance Level (a)** = 0.05   
Only 5% chance for Type I Error (false positive).
- **Statistical Power (b)** = 80%
The Minimal Detectable Effect (MDE) will be caught with 80% chance (20% chance for Type II Error: false negative).   

### Minimum Detectable Effect (MDE)

The test is aimed to detect a +0.5pp (percentage point) increase in conversion rate.

### Experiment Summary

- **Target cities:** Phuket, Krabi.
- **Unit of randomization:** User.
- **Primary metric:** Conversion Rate (CR).
- **Expected uplift (MDE):** +0.5pp
- **Significance level:** 5%.
- **Power:** 80%.

## 3. Risks and Mitigation

### Risks

Because the experiment involves users who choose both between channels, platforms and within the platform, in a marketplace environment, **interference between units** may affect experiment results. Users exposed to treatment (visibility boost in our case) may shift demand across properties or even cities, **affecting outcomes beyond treatment group**.   

This can skew control group results and even lead to demand redistribution:
- Within city: users book treated properties instead of control ones.
- Across cities: users change destinations toward cities with treated properties (e.g. Phuket vs Chiang Mai).

As a result, observed uplift at the property (or city) level may not reflect true increment in demand, but rather change of structure in existing demand (without change in total demand).   

Demand cannibalization isn't necessarily a negative phenomenon. Shifting demand toward higher-value inventory can improve overall platform performance, as long as revenue increase.

### Mitigation

To mitigate these effects:
- Results are aggregated at the city level.
- Total bookings and revenue are monitored alongside conversion rate. Level of "total" is fixed at Thailand level *(Bangkok, Chiang Mai, Krabi, Pattaya and Phuket in our case)*.
- Guardrail metrics (ADR, cancellation rate).
- In-depth after-test analytics to get more insights for relevant final business recommendations: Pareto (80/20), high vs low value properties, city-level segmentation.

## 4. Pre-test Design and Calculations

To successfully run A/B-test we need to know for how long it should be going, and it depends on **Sample Size (n)**. Sample Size should guarantee the Minimum Detectable Effect (MDE) will be detected with defined Significance Level and Statistical Power.

Link to Notebook with Test Design: [`01_ab_test_design.ipynb`](notebooks/01_ab_test_design.ipynb)

### Required Data

Data needed to compute required Sample Size:
- **Baseline** primary metric ($p_1$): current Conversion Rate.
- **MDE (Δ)**: minimum effect we want to detect, or Expected Uplift.
- **Significance Level (α)**: the risk of false positive.
- **Statistical Power (1-β)**: the chance of catching expected uplift if it exists.
- **Variance (var)**: how much data spreads out.   

> **Note:** Since `nomad_db` was created as a supply-side OTA dataset, it doesn't contain data regarding search sessions. That means steps of querying some data are skipped, we only assume those metrics.

### Inputs (including assumptions)

All the inputs with values:
- **Baseline Conversion Rate ($p_1$)** = 5% = 0.05 *(assumption)*
- **MDE (Δ)** = +10% = 0.05 * 0.1 = 0.005
- **Target Conversion Rate ($p_2$)** = $p_1$ + $\Delta$ = 0.055
- **Significance Level (α)** = 5%, it's Z-score (required for calculations) Zα = 1.96
- **Statistical Power (1-β)** = 80%, it's Z-score Zβ = 0.84

### Sample Size Calculations

First, we get **Variance** for conversion (binary metric):  

var =    
= $p_1$ $\times$ (1 - $p_1$) =    
= 0.05 $\times$ 0.95 = 0.0475    

Then, use two-proportion z-test sample size formula to get **Sample Size (n)** per group:  
 
n (per group) =    
= 2 $\times$ (Zα + Zβ)$^2$ $\times$ $p_1$ $\times$ (1 - $p_1$) / $\Delta^2$ =   
= 2 $\times$ (Zα + Zβ)$^2$ $\times$ var / $\Delta^2$ =    
= 2 $\times$ (2.8)$^2$ $\times$ 0.0475 / 0.005$^2$ $\approx$ 29,792   

**Sample Size (n):**   
$\approx$ **30,000** users per group    
$\approx$ **60,000** total users   

### Estimated Experiment Duration

Converting sample size into time needed to get it. We need a daily users in Phuket and Krabi. Since `nomad_db` doesn't have search-side data, we need another assumption.   

> **NOTE:** All assumptions are MVP project allowed only. README contains all the information needed to get (calculate, fetch) every single value.   

Let's assume:
- **Average Daily Users**, Phuket = 5,000 users
- **Average Daily Users**, Krabi = 5,000 users

**Daily Users (daily_users)** = 5000 + 5000 = 10,000 users.  

Since we have two groups (control and treatment), **Estimated Experiment Duration(days)**:   

days = n(per group) / (daily_users / 2) =   
= 30000 / (10000 / 2) = 6 days   

**Estimated Experiment Duration(days)** = 6 days.   
But, due to weekday vs weekend effect, noise and user behavior variability, it's better to have at least a week+ duration: **10-14 days**.   

## 5. A/B-test Simulation

Since there's no actual experiment behind the project, and `nomad_db` doesn't contain it's data, we **simulate experimental data** that mimics Control group (no visibility boost) and Treatment group (visibility boost applied to get higher Conversion Rate).   
All the needed assumptions were introduced (or calculated) in step 4 "Pre-test Design and Calculations". 

Simulation Notebook: [`02_simulation.ipynb`](notebooks/02_simulation.ipynb)   

### About Simulation

We simulate **user-level binary outcomes** (instances of session events):   
**user_id** (index) | **group** | **conversion**   

```code
session -> 0 (no booking)
session -> 1 (booking)
```

### Simulation

Each user was simulated separately: 
- It begins with generating Sample Size (n) per group Control group outcomes (0 and 1) with probability $p_1$ (control Conversion Rate), and Sample Size (n) per group Treatment group outcomes (0 and 1) with probability $p_2$ (Expected Conversion Rate after visibility boost).   
```python
control = np.random.binomial(1, p_control, n_per_group)
treatment = np.random.binomial(1, p_treatment, n_per_group)
```
- Generated Control and Treatment series were concatenated into column `conversion`.
- After that series of 'control' and 'treatment' string values of the same length were generated and concatenated into column `group`.
- Columns `group` and `conversion` converted into a DataFrame, where `index` represents `user_id`.   
```python
sessions_df = pd.DataFrame({
    "group": ["control"] * n_per_group + ["treatment"] * n_per_group,
    "conversion": np.concatenate([control, treatment])
})
```

### Observed Results (Simulation Check)

Results of the simulation:
```code
cr_control               0.049822
cr_treatment             0.054248
sample_size_per_group    29826
total_sample_size        59652
days                     14
relative_lift            0.08883    
```

Results fully comply with the conditions of A/B-test simulation. Simulation raw data written to database's `analytics` schema: `analytics.ab_test_simulation_v1`.

## 6. Statistical Testing

Experiment metrics:
- p_control = cr_control: Control group Conversion Rate.
- p_treatment = cr_treatment: Treatment group Conversion Rate.
- n_control = n_treatment = sample_size_per_group: Sample Size of Control and Treatment groups.   

> **Goal:** reject or accept Null Hypothesis.   

Analytical Notebook: [`03_analysis.ipynb`](notebooks/03_analysis.ipynb)

### 6.1. Hypotheses

```code
H0 (null):          p_treatment  = p_control    (no effect)
H1 (alternative):   p_treatment != p_control    (effect exists)
```   

### 6.2. Observed Metrics

|**Group**|**Conversion Rate**|**Sample Size**|
|:-|:-|:-|
| **Control** | 0.0498 | 29826 |
| **Treatment** | 0.0542 | 29826 |

### 6.3. Analysis

First, we get **Observed Difference (delta)**:   
```python
delta_observed = p_treatment - p_control
delta_observed = 0.0542 - 0.0498 = 0.0044
```

### Statistical Significance

Is delta of **0.0044 (0.44 pp)** big enough compared to noise? It should be compared to **Standard Error (SE)**:   

$` SE = \sqrt{\text{p\_pool} \times (1 - \text{p\_pool}) \times (\frac{1}{\text{n\_control}} + \frac{1}{\text{n\_treatment}} )} `$

where: `p_pool` - is **pooled conversion rate**:   

$` \text{p\_pool} = \frac{(\text{p\_control} \times \text{n\_control}) + (\text{p\_treatment} \times \text{n\_treatment})}{\text{n\_control} + \text{n\_treatment}} `$

After that, we need **Z-score** (how many "noise units" (standard errors) away we are from 0) to finally get **p-value** and make a decision about **Statistical Significance** of observed results (delta).  

$` \text{Z-score} = \frac{\text{delta\_observed}}{se} `$

How it looks in Python/Pandas:
```python
p_pool = (
    (p_control * n_control + p_treatment * n_treatment)
    / (n_control + n_treatment)
)

se = np.sqrt(
    p_pool * (1 - p_pool)
    * (1/n_control + 1/n_treatment)
)

z = delta_observed / se
```

**Result:** se = 0.0018, z-score = 2.43   

Using `scipy.stats` library to get **p-value** for z-score:
```python
from scipy.stats import norm

p_value = 2 * (1 - norm.cdf(abs(z)))
```

> **Result:** p-value = 0.015   

At this point we have to make a decision about **statistical** significance of observed delta between conversion rates. To make, we $\alpha$ from test design input metrics ($\alpha = 0.05$) and compare it to **p-value**:

| **Result** | **Meaning** |
|:-|:-|
| p < $\alpha$ | Observed uplift is statistically significant and unlikely due to random variation |
| p $\geq$ $\alpha$ |effect is probably due to random variation |   

**Decision**   

0.015 < 0.05
> **The observed difference 0.0044 (0.44%) is statistically significant.**  

### Confidence Interval (CI)

Here we calculate Confidence Interval (CI) for our Significance Level ($\alpha = 0.05$).  

$$ CI = delta \pm \frac{Z\alpha}{2} \times SE $$

**Results:** [0.09 pp ; 0.79 pp]    

### Statistical Interpretation

The observed uplift of **+0.44 pp** is **statistically significant** (p_value = 0.015 < 0.05).   
The **95% confidence interval [0.09 pp ; 0.79 pp]** lies entirely above zero, which indicates a **robust positive effect** of the experiment.

# 7. Business Interpretation

## 7.1. Summary of the Experiment

The goal of A/B-test was a **visibility boost** testing for the properties:
- Location: Phuket, Krabi (Thailand)
- Decline Profile: DEMAND_CRISIS   

### Key outcomes:

- **Absolute uplift:** +0.44 percentage points
- **Relative uplift:** +8.8%
- **Statistical significance:**
    - p-value = 0.015 < 0.05: **significant**
- **95% Confidence Interval (CI) of the Effect:**
    - Absolute: **[+0.09 pp ; +0.79 pp]**
    - Relative: **[+1.8% ; +15.9%]**

### Visual Summary of Conversion Rate Uplift

![A/B Test Results: Conversion Rate Comparison](/outputs/conversion_rates.png)   
*Figure 1: Conversion rates with 95% confidence interval ($\alpha = 0.05$). Treatment shows +0.44pp absolute uplift (+8.8% relative). The confidence intervals partially overlap (control: [4.63%, 5.33%]; treatment: [5.07%, 5.77%]), but the p-value of 0.015 confirms statistical significance.*

## 7.2. Interpretation of the Effect

The experiment demonstrates a **statistically significant and positive impact** on Conversion Rate:
- The entire confidence interval (CI) lies above zero, that means the effect is robust and not driven by noise.
- Even the worst case scenario (CI Lower Band = +1.8%) the uplift is positive, what limits a downside risk.

This strongly suggests that **visibility is a real bottleneck** in Phuket and Krabi, results are consistent with Thailand Market Equilibrium and Drift framework findings (`DEMAND_CRISIS`).

## 7.3. Secondary Metric and Business Impact

To evaluate revenue impact **RevPAR** was declared as a **Secondary Metric** of the testing. As was stated in **Step 5: A/B-test Simulation**, the only data was "collected" *(generated)* is sessions with conversions. Obviously, real experiment affects the whole performance, not only conversion rates, but occupancy, prices, cancellations, may lead to change in available units, and sure shifts aggregated metrics like ADR, RevPAR etc.   

The best solution is to compare metrics at three layers: baseline (pre-test), control group, and treatment group. Adding the levels of aggregation, like city, market, country ensures most of the shifts inflicted by an experiment (see Step 3: Risk and Mitigation) will be detected.   

For current experiment limitations too many assumptions are required for a complete in-depth Business Impact analysis. In real case we'd query the next raw level data:
- grain:
    - country
    - city
    - property
- A/B-test boolean flags:
    - control group
    - treatment group
- bookings fact data (period: 4-weeks prior test + test period):
    - reservation date (created date)
    - reservation_id
    - price per night
    - available units (total)
    - commission rate
    - booking status
    - channel_id

And then aggregate it for the needed levels (property, city, test-market vs other market, country, weekdays vs weekends etc) of metrics:
- Conversion Rate
- available units
- booked units
- Revenue
- ADR
- Occupancy
- RevPAR
- Cancellation Rate

This data will allow to get insights about how **Visibility Boost** really affected the market:
- We get positive CR uplift, but did we get Revenue and RevPAR positive uplift?
- What happened with Commissions?
- Did we observe overall Demand Increment (new users) or just shift between cities/properties?
- Was effect concentrated around weekdays or weekends?
- Did ADR shift?
- Did Cancellation Rate increase (both: control and treatment groups)?

After that, more efficient roll out can be achieved by smart segmentation. Regarding expected Business Impact, it can be calculated by applying metrics uplifts to roll out market.

## 7.4. Risk Assessment

Despite strong results, several risks must be monitored:   
1. **Cannibalization.** Demand may shift to boosted properties from other ones. That means net market gain could be lower than observed uplifts.   
**How to mitigate:** Monitor **total city bookings**, not only treated properties.   
2. **Price shift (ADR risk)**. Increased visibility may stimulate discounting.   
**How to mitigate:** Track **ADR stability.**   
3. **Long-term sustainability:** Effect of visibility boost may (and will) decay over time.   
**How to mitigate:** Post-launch monitoring.

## 7.5. Final Decision

> **ROLLOUT** on chosen segments.    

### Steps
1. **Gradual rollout**: start with the most promising segments. Expand if stable.
2. **Post-launch monitoring**: Conversion rate, RevPAR, ADR, Cancellation Rate, Total bookings (anti-cannibalization).
3. **Fine-tune:** optimize visibility boost activities.