"""
Streamlit GUI for Stroke Dataset Analysis
Beautifully styled with consistent design, fonts, colors, and spacing.
"""

# ---------- Imports ----------
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from dataset_module import load_data
from query_module import (
    query_smokers_hypertension_stroke,
    query_heart_disease_stroke,
    query_hypertension_gender_stroke,
    query_smoking_stroke,
    query_residence_stroke,
    query_dietary_habits_stroke,
    query_hypertension_stroke_patients,
    query_hypertension_stroke_comparison,
    query_heart_disease_stroke_patients,
    query_descriptive_statistics,
    query_average_sleep_hours_stroke
)

# ---------- Helper Functions ----------

def format_output(result):
    if isinstance(result, dict):
        if 'message' in result:
            return result['message']
        output = []
        for key, value in result.items():
            if isinstance(value, dict):
                output.append(f"### {key}")
                for sub_key, sub_value in value.items():
                    output.append(f"- **{sub_key}:** {sub_value}")
            elif isinstance(value, list):
                output.append(f"### {key} ({len(value)} records)")
            else:
                output.append(f"- **{key}:** {value}")
        return "\n".join(output)
    elif isinstance(result, list):
        return f"### Found {len(result)} records."
    return str(result)

def create_histogram(data, feature, title):
    fig = px.histogram(
        x=data,
        nbins=30,
        title=title,
        labels={'x': feature, 'count': 'Count'},
        template='plotly_dark',
        color_discrete_sequence=['#00BFFF']
    )
    fig.update_layout(
        xaxis_title=feature,
        yaxis_title="Count",
        bargap=0.2
    )
    return fig

def create_bar_chart(categories, values, title, x_label, y_label):
    fig = go.Figure(data=[
        go.Bar(x=categories, y=values, marker_color='#FF7F50')
    ])
    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template='plotly_dark',
        plot_bgcolor='#111111',
        paper_bgcolor='#111111'
    )
    return fig

def custom_header(title):
    st.markdown(
        f"<h1 style='text-align: center; color: #FF4B4B; font-family: Arial;'>{title}</h1>",
        unsafe_allow_html=True
    )
    st.write("---")

# ---------- Main App ----------

def run_streamlit_app(filepath):
    st.set_page_config(
        page_title="Stroke Dataset Analysis",
        page_icon="🧠",
        layout="wide"
    )

    # Header
    custom_header("🧠 Stroke Dataset Query & Visualization System")

    with st.spinner('Loading data...'):
        try:
            data, header = load_data(filepath)
            if not data:
                st.error("❌ No data loaded. Please check the file path.")
                return
            st.success(f"✅ Dataset loaded successfully! {len(data)} records available.")
        except Exception as e:
            st.error(f"❌ Failed to load dataset: {e}")
            return

    # Sidebar
    st.sidebar.title("🔍 Choose Your Query")
    query = st.sidebar.selectbox(
        "Select a Query:",
        [
            "Select a query",
            "Smokers with Hypertension (Stroke)",
            "Heart Disease with Stroke",
            "Hypertension by Gender (Stroke vs No Stroke)",
            "Smoking Habits (Stroke vs No Stroke)",
            "Urban vs Rural (Stroke)",
            "Dietary Habits (Stroke vs No Stroke)",
            "Hypertension Patients (Stroke)",
            "Hypertension Patients (Stroke vs No Stroke)",
            "Heart Disease Patients (Stroke)",
            "Descriptive Statistics",
            "Sleep Hours (Stroke vs No Stroke)"
        ]
    )

    # Main Content
    st.markdown("### 📊 Query Results and Visualizations")
    st.info("Select a query from the sidebar to view dynamic analysis and charts. Results can also be saved as CSV files.")

    if query == "Select a query":
        st.warning("Please select a query to begin.")
        return

    # Handle each query
    try:
        if query == "Smokers with Hypertension (Stroke)":
            result = query_smokers_hypertension_stroke(data)
            st.subheader("🚬 Smokers with Hypertension (Stroke)")
            st.markdown(format_output(result))
            if 'average_age' in result:
                fig = create_bar_chart(
                    ['Average Age', 'Median Age'],
                    [result['average_age'], result['median_age']],
                    "Age Statistics",
                    "Statistic", "Age"
                )
                st.plotly_chart(fig)

        elif query == "Heart Disease with Stroke":
            result = query_heart_disease_stroke(data)
            st.subheader("❤️ Heart Disease with Stroke")
            st.markdown(format_output(result))
            if 'average_age' in result:
                fig = create_bar_chart(
                    ['Average Age', 'Average Glucose Level'],
                    [result['average_age'], result['average_glucose_level']],
                    "Heart Disease Stroke Statistics",
                    "Statistic", "Value"
                )
                st.plotly_chart(fig)

        elif query == "Hypertension by Gender (Stroke vs No Stroke)":
            result = query_hypertension_gender_stroke(data)
            st.subheader("🧍‍♂️🧍‍♀️ Hypertension by Gender")
            st.markdown(format_output(result))
            categories, values = zip(*[
                (k, v['average_age']) for k, v in result.items() if 'average_age' in v
            ])
            fig = create_bar_chart(
                categories, values,
                "Average Age by Gender & Stroke Status",
                "Group", "Average Age"
            )
            st.plotly_chart(fig)

        elif query == "Smoking Habits (Stroke vs No Stroke)":
            result = query_smoking_stroke(data)
            st.subheader("🚬 Smoking Habits (Stroke vs No Stroke)")
            st.markdown(format_output(result))
            categories, values = zip(*[
                (k, v['average_age']) for k, v in result.items() if 'average_age' in v
            ])
            fig = create_bar_chart(
                categories, values,
                "Smoking Status by Stroke Outcome",
                "Group", "Average Age"
            )
            st.plotly_chart(fig)

        elif query == "Urban vs Rural (Stroke)":
            result = query_residence_stroke(data)
            st.subheader("🏙️🏡 Urban vs Rural Stroke")
            st.markdown(format_output(result))
            categories, values = zip(*[
                (k, v['average_age']) for k, v in result.items() if 'average_age' in v
            ])
            fig = create_bar_chart(
                categories, values,
                "Average Age: Urban vs Rural",
                "Residence Type", "Average Age"
            )
            st.plotly_chart(fig)

        elif query == "Dietary Habits (Stroke vs No Stroke)":
            result = query_dietary_habits_stroke(data)
            st.subheader("🥗 Dietary Habits")
            st.markdown(format_output(result))
            if 'stroke' in result:
                fig = create_bar_chart(
                    list(result['stroke'].keys()),
                    list(result['stroke'].values()),
                    "Dietary Habits of Stroke Patients",
                    "Habit", "Count"
                )
                st.plotly_chart(fig)

        elif query == "Hypertension Patients (Stroke)":
            result = query_hypertension_stroke_patients(data)
            st.subheader("💉 Hypertension Patients (Stroke)")
            st.markdown(format_output(result))
            ages = [r['Age'] for r in result if isinstance(r['Age'], (int, float))]
            if ages:
                fig = create_histogram(ages, "Age", "Age Distribution: Hypertension with Stroke")
                st.plotly_chart(fig)

        elif query == "Hypertension Patients (Stroke vs No Stroke)":
            result = query_hypertension_stroke_comparison(data)
            st.subheader("💉 Hypertension (Stroke vs No Stroke)")
            st.markdown(format_output(result))
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=[r['Age'] for r in result['hypertension_led_to_stroke']],
                name="Stroke",
                opacity=0.6
            ))
            fig.add_trace(go.Histogram(
                x=[r['Age'] for r in result['hypertension_did_not_lead_to_stroke']],
                name="No Stroke",
                opacity=0.6
            ))
            fig.update_layout(
                barmode='overlay',
                title="Age Distribution: Hypertension (Stroke vs No Stroke)",
                template='plotly_dark'
            )
            st.plotly_chart(fig)

        elif query == "Heart Disease Patients (Stroke)":
            result = query_heart_disease_stroke_patients(data)
            st.subheader("❤️ Heart Disease (Stroke Patients)")
            st.markdown(format_output(result))
            ages = [r['Age'] for r in result if isinstance(r['Age'], (int, float))]
            if ages:
                fig = create_histogram(ages, "Age", "Age Distribution: Heart Disease with Stroke")
                st.plotly_chart(fig)

        elif query == "Descriptive Statistics":
            st.subheader("📈 Descriptive Statistics")
            feature = st.text_input("🔎 Enter a feature name:", key="feature_input")
            if feature:
                result = query_descriptive_statistics(data, feature, header)
                st.markdown(format_output(result))
                numbers = [record[feature] for record in data if isinstance(record[feature], (int, float))]
                if numbers:
                    fig = create_histogram(numbers, feature, f"Distribution of {feature}")
                    st.plotly_chart(fig)

        elif query == "Sleep Hours (Stroke vs No Stroke)":
            result = query_average_sleep_hours_stroke(data)
            st.subheader("😴 Sleep Hours (Stroke vs No Stroke)")
            st.markdown(format_output(result))
            if 'stroke_patients' in result and 'non_stroke_patients' in result:
                fig = create_bar_chart(
                    ['Stroke Patients', 'Non-Stroke Patients'],
                    [result['stroke_patients']['mean'], result['non_stroke_patients']['mean']],
                    "Average Sleep Hours",
                    "Group", "Hours"
                )
                st.plotly_chart(fig)

    except Exception as e:
        st.error(f"❌ Query failed: {e}")

# ---------- Run App ----------

if __name__ == "__main__":
    FILEPATH = "data.csv"
    run_streamlit_app(FILEPATH)
