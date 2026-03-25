# A/B-test Visibility Boost based on Thailand OTA Market Equilibrium and Drift

## 1. Context and Problem

Thailand OTA market dynamics across main cities *(Bangkok, Chiang Mai, Krabi, Pattaya and Phuket)* were analyzed using the [Market Equilibrium and Drift (MED)](https://github.com/SuslovAnton/ota-market-equilibrium-and-drift) framework.   
Results show that **Phuket** and **Krabi** are currently in a `PRICE_WAR` macro phase. However, RevPAR decline decomposition reveals that the drop is primarily `OCC_LED` (occupancy led) with ~90% occupancy contribution. That points towards `DEMAND_CRISIS` decline profile and a **demand-side problem** rather than pricing fault.    

Therefore, an A/B-test was designed to evaluate if increasing property visibility can improve conversion rates in Phuket and Krabi markets, dragging **Occupancy** and **RevPAR** higher.


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
    - **Conversion Rate (CR):** share of users who complete a booking.
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

