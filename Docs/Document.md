# Business Question
Which clinical study strategy offers the most suitable balance between operational feasibility, timeline and cost under a given set of study requirements and constraints?
How does the result distribution change when we modify oprational decisions?

# Project Rationale
Clinical study planning involves decisions under uncertainty. Recruitment forecasts, site activation timelines and operational costs are commonly estimated using assumptions that may not fully reflect the variability of real-world study execution.

Evaluating a strategy against a single set of assumptions can obscure the range of plausible outcomes and the risk of missing predefined targets. Furthermore, increasing operational resources does not necessarily translate into proportional improvements in recruitment or study duration.

This project explores how scenario analysis and probabilistic simulation can support more informed clinical study planning. By modelling alternative execution strategies under a consistent set of assumptions, the simulator attempts to illustrate how operational decisions influence recruitment performance, timelines and costs, while making uncertainty and model limitations explicit.

# Variables
## Study Parameters
- Target sample size: n° of patients to be recruited
- Max recruitment period : maximum acceptable recruitment duration (months)
- Max study budget: max allowable study cost 


## Strategy variables
- N° of sites : n° of sites to be included
- Site activation time: time required for sites to become operational
- Site recruitment rate : expected participants recruited per active site per month
- start up cost: cost associated with initiating a site
- Site operating cost: cost per site per month
- Site risk level: risk classification assigned to each hypothetical site
---activation delay: expected deviation from the planned site activation timeline
---recruitment performance: expected recruitment performance relative to the site's assigned recruitment target
---operational reliability: estimated likelihood of meeting predefined operational milestones

## Simulation outputs
- Estimated recruitment duration : simulated time required to reach the target sample size
- Estimates total cost : estimated cost based on the cost components included in the model
- Probability of meeting timeline : proportion of simulation iterations completed within the recruitment deadline
- Probability of staying within budget : proportion of iterations in which estimated costs remain within the budget
- Strategy risk exposure: assessment of the selected site's risk composition and its simulated consequences for recruitment timelines and costs.


# Approach and tools 
## Data and Materials
The project will use synthetic study-level and site-level data generated programmatically in Python. The data will represent hypothetical clinical study parameters, site activation times, recruitment performance and operational costs.

The synthetic dataset will be designed to reproduce plausible operational relationships for exploratory modelling purposes. It will not be presented as observed clinical trial data or as a validated representation of any specific therapeutic area.

## Modelling Approach
A scenario-based simulation framework will be developed to compare alternative study execution strategies under consistent study requirements.

A Monte Carlo simulation will represent uncertainty in selected operational parameters, such as site activation times and recruitment rates. Each simulation iteration will generate a possible study execution outcome based on the specified assumptions and decision variables.

Recruitment duration will be estimated from the cumulative recruitment achieved by active sites until the target sample size is reached. Operational costs will be calculated using explicitly defined cost components and their associated assumptions.

The results will be compared across scenarios using distributions of recruitment duration and estimated cost, together with the probability of meeting predefined operational targets. Sensitivity analysis will be used to assess which assumptions and decision variables have the greatest influence on the simulated outcomes.

## Tools
Python, pandas, NumPy, Streamlit and Plotly will be considered for data generation, simulation, analysis and interactive visualisation.

# Scope
## In scope
- Compare alternative clinical study execution strategies.
- Simulate uncertainty in site activation and patient recruitment.
- Estimate recruitment timelines and defined operational costs.
- Assessthe probability of meeting predefined recruitment, timeline and budget targets.
- Sensitivity analysis to identify influential assumptions and decision variables.
- Interactive visualisation of scenario outcomes and operational trade-offs.

## Out of Scope
- Prediction of actual clinical trial outcomes using validated historical datasets.
- Patient-level recruitment modelling or individual patient eligibility prediction.
- Clinical efficacy, safety or regulatory outcome prediction.
- Full clinical trial budgeting or detailed country-specific cost estimation.
- Site selection based on verified real-world site performance.

# Limitations

The simulator will rely on synthetic data and predefined modelling assumptions rather than observed clinical trial outcomes. Its results will therefore illustrate the behaviour of the model under specified conditions and should not be interpreted as empirically validated forecasts.
The model may also omit relevant factors, including competition for eligible patients, country-specific operational differences, protocol amendments, site initiation delays beyond the modelled distributions and changes in recruitment performance over time.
Scenario comparisons will be conditional on the model structure and its assumptions. A strategy that performs better in the simulation cannot automatically be considered superior in a real clinical study.

# Strategies
## Lean
- Low investment
- Small site network
- Standard activation approach
- Accept longer timeline when the additional cost of acceleration is not justified
- Risk approach -> prefer cost efficiency and predictable execution

## Balanced
- Moderate investment
- Intermediate site network
- Activation selectively prioritized
- Balance time and cost, operational costs and risk exposure
- Balance risk and capacity (appropriate trade-off between recruitment capacity and operational complexity)

## Accelerated
- high investment
- Larger site network and/or additional resources to expedite site activation
- activation acelerated through additional resources
- Prioritises shorter recruitment timelines and faster achievement of study milestones
- accept hight risk if it helps reducing delays 