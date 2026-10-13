import pandas as pd
import streamlit as st
import plotly.express as px

####LOAD DATA 
@st.cache_data
def load_data():
    sites = pd.read_csv("data/sites_data.csv")
    clinical_profiles = pd.read_csv("data/clinical_site_profiles.csv")
    risks = pd.read_csv("data/risks.csv")

    return sites, clinical_profiles, risks
sites, clinical_profiles, risks = load_data()

#Config page
st.set_page_config(
    page_title="Site Selection & Strategy Evaluator",
    layout="wide"
)


st.title("Site Selection & Strategy Evaluator")
st.caption("Explore site selection strategies and their trade-offs using synthetic clinical trial data")



######## SECTION 1#####
st.header("1. Study requirements")

col1, col2, col3 = st.columns(3)
#country
with col1:
    countries = sorted(clinical_profiles["country"].dropna().unique())
    selected_country = st.multiselect("Country", countries)
    country_profiles = clinical_profiles.copy()

    if selected_country:
        country_profiles = country_profiles[
        country_profiles["country"].isin(selected_country)
    ]

#TA
with col2:
    areas = sorted(country_profiles["therapeutic_area"].dropna().unique())
    selected_area = st.multiselect("Therapeutic area", areas)

    area_profiles = country_profiles.copy()

    if selected_area:
        area_profiles = area_profiles[
        area_profiles["therapeutic_area"].isin(selected_area)
    ]

#indication
with col3:
    indications = sorted(area_profiles["indication"].dropna().unique())
    selected_indication = st.multiselect("Indication", indications)

    filtered_profiles = area_profiles.copy()

    if selected_indication:
        filtered_profiles = filtered_profiles[
        filtered_profiles["indication"].isin(selected_indication)
    ]

results = filtered_profiles.merge(
    sites,
    on=["site_id", "country"],
    how="left",
    validate="many_to_one"
)

results = results.merge(
    risks[["site_id", "risk_level"]],
    on="site_id",
    how="left",
    validate="many_to_one"
)



##########SECTION 2#########
st.header("2. Site landscape")
all_filtered_sites = clinical_profiles.copy()

if selected_country:
    all_filtered_sites = all_filtered_sites[
        all_filtered_sites["country"].isin(selected_country)
    ]

available_sites = all_filtered_sites["site_id"].nunique()
eligible_sites = filtered_profiles["site_id"].nunique()

col1, col2 = st.columns(2)

with col1:
    st.metric("Available sites", available_sites)

with col2:
    st.metric("Sites matching requirements", eligible_sites)


#####SETION 3 ####

st.header("3. Site comparison")

chart_data = results.drop_duplicates(
    subset="site_id"
).copy()

######scatter####
fig = px.scatter(
    chart_data,
    x="act_timeline",
    y="op_reliab",
    size="expected_recruit_rate",
    color="risk_level",
    hover_name="site_id",
    hover_data=[
        "country",
        "expected_recruit_rate",
        "act_timeline",
        "op_reliab",
        "risk_level"
    ],
    labels={
        "act_timeline": "Activation timeline (days)",
        "op_reliab": "Operational reliability",
        "expected_recruit_rate": "Recruitment potential",
        "risk_level": "Operational risk"
    },
    title="Operational reliability vs. activation time",
    subtitle=("Bigger dots show higher recruitment potential")
)
fig.update_xaxes(
    range=[20, 110],
    tickmode="linear",
    tick0=10,
    dtick=10
)

st.plotly_chart(fig, use_container_width=True)


#### SECTION 4 ####
strategy_data = sites.merge(
    risks[["site_id", "risk_level"]],
    on="site_id",
    how="left",
    validate="one_to_one"
)

risk_priority = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

strategy_data["risk_priority"] = (
    strategy_data["risk_level"].map(risk_priority)
)
eligible_site_ids = filtered_profiles["site_id"].unique()
strategy_data = strategy_data[
    strategy_data["site_id"].isin(eligible_site_ids)
].copy()

st.header("4. Site selection strategies")
if st.toggle("Strategy priorities and trade-offs", value=False):
    st.markdown("""
    - **Conservative:** Prioritises lower risk and higher reliability. Trade-off: timeline ≥ 91 days.
    - **Balanced:** Prioritises lower costs within a defined activation timeline. Trade-offs: higher risk and moderate timelines.
    - **Accelerated:**  Prioritises faster activation and higher recruitment performance. Trade-off: highest costs.
    """)

n_sites = st.number_input(
    "Number of sites to select",
    min_value=1,
    max_value=int(sites["site_id"].nunique()),
    value=10,
    step=1
)

### Code recycled from notebook 03

strategies = {
    "Conservative": {
        "max_risk": 1,
        "min_delay": 71,
        "sort_by": ["risk_priority", "op_reliab"],
        "ascending": [True, False]
    },
    "Balanced": {
        "max_risk": 3,
        "min_delay": 41,
        "max_delay": 70,
        "sort_by": ["startup_cost", "month_op_cost", "risk_priority"],
        "ascending": [True, True, True]
    },
    "Accelerated": {
        "max_risk": 2,
        "max_delay": 40,
        "sort_by": ["rec_perf_ratio", "op_reliab"],
        "ascending": [False, False]
    }
}


def select_sites(data, strategy_name, n_sites):
    strategy = strategies[strategy_name]

    eligible_sites = data.copy()
    eligible_sites = eligible_sites[
        eligible_sites["risk_priority"] <= strategy["max_risk"]
    ]

    if "min_delay" in strategy:
        eligible_sites = eligible_sites[
            eligible_sites["act_timeline"] >= strategy["min_delay"]
        ]
    if "max_delay" in strategy:
        eligible_sites = eligible_sites[
            eligible_sites["act_timeline"] <= strategy["max_delay"]
        ]

    selected_sites = (
        eligible_sites
        .sort_values(
            by=strategy["sort_by"],
            ascending=strategy["ascending"]
        )
        .head(int(n_sites))
        .copy()
    )

    return selected_sites

####Sites compare
strategy_results = {}

for strategy_name in strategies:
    strategy_results[strategy_name] = select_sites(
        strategy_data,
        strategy_name,
        n_sites
    )

col1, col2, col3 = st.columns(3)

for col, (strategy_name, selected) in zip(
    [col1, col2, col3],
    strategy_results.items()
):
    with col:
        st.subheader(strategy_name)
        st.metric("Sites selected", len(selected))
        st.metric(
            "Median activation (days)",
            f"{selected['act_timeline'].median():.0f}"
            if not selected.empty else "—"
        )
        st.metric(
            "Median operational reliability",
            f"{selected['op_reliab'].median():.2f}"
            if not selected.empty else "—"
        )
        st.metric(
            "Total startup cost",
            f"{selected['startup_cost'].sum():,.0f}"
        )
        st.metric(
            "Total monthly operating cost",
            f"{selected['month_op_cost'].sum():,.0f}"
        )
        if selected.empty:
            st.warning("No sites meet the eligibility criteria.")
        elif len(selected) < n_sites:
            st.info(
                f"Only {len(selected)} eligible sites available "
                f"out of {n_sites} requested."
            )








#### SECTION 5####
st.header("5. Site selection results")

for strategy_name, selected in strategy_results.items():
    st.subheader(strategy_name)
    # Add clinical information for the selected sites
    clinical_info = (
        filtered_profiles[
            ["site_id", "country", "therapeutic_area", "indication"]
        ]
        .drop_duplicates(subset=["site_id", "country"])
    )
    selected_table = selected.merge(
        clinical_info,
        on=["site_id", "country"],
        how="left",
        validate="one_to_one"
    )
    columns_to_show = [
        "site_id",
        "country",
        "therapeutic_area",
        "indication",
        "expected_recruit_rate",
        "act_timeline",
        "op_reliab",
        "startup_cost",
        "month_op_cost",
        "risk_level"
    ]
    st.dataframe(
        selected_table[columns_to_show].sort_values(
            by=["risk_level", "expected_recruit_rate"],
            ascending=[True, False]
        ),
        use_container_width=True,
        hide_index=True
    )

st.divider()

if st.toggle("Show model limitations"):
    st.markdown("""
    - **Synthetic data:** results are illustrative and do not represent real clinical trial sites.
    - **Unvalidated rules:** risk categories and selection criteria are predefined and have not been validated.
    - **Fixed eligibility criteria:** strategies may return fewer sites than requested, or no eligible sites. No relaxation rules applied.
    - **Simplified estimates:** recruitment performance, activation timelines and costs are modelled for demonstration purposes only.
    """)
