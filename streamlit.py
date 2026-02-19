import streamlit as st
import pandas as pd
import pymysql
from sqlalchemy import create_engine

host = "localhost"
user = "root"
password = "12345"
database = "eq_project"

engine = create_engine("mysql+pymysql://root:12345@localhost/eq_project")

queries = {
    
    "1. Top 10 strongest earthquakes (mag)": """
        select id, place, time, mag from earthquakes order by mag desc LIMIT 10;
    """,

    "2. Top 10 deepest earthquakes (depth_km)": """
        select id, place, time, mag from earthquakes order by depth_km desc LIMIT 10;
    """,

    "3. Shallow earthquakes < 50 km and mag > 7.5": """
        select id, place, time, mag, depth_km from earthquakes
        where depth_km < 50 and mag > 7.5;
    """,

    "5. Average magnitude per magnitude type (magType)": """
        select magType, round(avg(mag), 2) as average, count(*) as total_number 
        from earthquakes where mag is not null
        group by magType order by average desc;
    """,

    "6. Year with most earthquakes": """
        select extract(year from time) as year, count(*) as earthquake_frequency
        from earthquakes group by year order by earthquake_frequency desc limit 1;
    """,

    "7. Month with highest number of earthquakes": """
        select monthname(time) as month, count(*) as earthquake_frequency
        from earthquakes group by month order by earthquake_frequency desc limit 1;
    """,

    "8. Day of week with most earthquakes": """
        select dayname(time) as day, count(*) as earthquake_frequency
        from earthquakes group by day order by earthquake_frequency desc limit 1;
    """,

    "9. Count of earthquakes per hour of day": """
        select hour(time) as per_hour, count(*) as earthquake_frequency
        from earthquakes group by per_hour order by earthquake_frequency asc;
    """,

    "10. Most active reporting network (net)":"""
        select net as network, count(*) as active_reports
        from earthquakes group by network order by active_reports desc limit 1;
    """,

    "11. Top 5 places with highest casualties": """
        select place, max(felt) as casualities from earthquakes
        group by place order by casualities desc limit 5;
        """,

    "14. Count of reviewed vs automatic earthquakes (status)": """
        select status, count(*) as total_earthquakes
        from earthquakes group by status order by total_earthquakes desc;
    """,

    "13. Economic Loss by alert level": """
        select alert as economic_loss, count(*) as count from earthquakes group by alert;
    """,

    "15. Count by earthquake type": """
        select type as earthquake_type, count(*) as total_earthquakes
        from earthquakes group by earthquake_type order by total_earthquakes desc;
    """,

    "16. Number of earthquakes by data type": """
        select types as data_type, count(*) as number_of_earthquakes
        from earthquakes group by data_type order by number_of_earthquakes desc;
    """,

    "18. Events with high station coverage (nst > threshold)": """
        select id, mag, place, nst from earthquakes where nst > 100  order by nst desc limit 10;
    """,

    "19. Number of tsunamis triggered per year": """
        select year(time) as year, count(*) as total_tsunami from earthquakes
        where tsunami = 1 group by year;
    """,

    "20. Count earthquakes by alert levels": """
        select alert, count(*) as total_earthquakes from earthquakes where alert is not null
        group by alert order by total_earthquakes desc;
    """,

    "21. Top 5 countries with highest average magnitude": """
        select country, round(avg(mag), 2) as average_magnitude, count(*) as total
        from earthquakes group by country order by average_magnitude desc limit 5;
    """,

    "22. Countries that experienced both shallow and deep earthquakes within the same month": """
        select place from earthquakes group by place, year(time), month(time)
        having sum(depth_km < 70) > 0 and sum(depth_km > 300) > 0;
    """,

    "23. Year-over-year growth rate in the total number of earthquakes globally": """
        select year, total, lag(total) over (order by year) as prev_year,
        round(((total - lag(total) over (order by year)) /  lag(total) over (order by year)) * 100, 2) as growth_rate
        from (select year(time) as year, count(*) as total from earthquakes group by year) as yearly;
    """,

    "24. 3 most seismically active regions by combining both frequency and average magnitude":"""
        select place as region, count(*) as frequency, round(avg(mag), 2) as average_magnitude
        from earthquakes group by region having frequency >= 10 order by average_magnitude, frequency desc limit 3;
    """,

    "25. Countrywise average depth of earthquakes within ±5° latitude range of the equator": """
        select country, round(avg(depth_km), 2) as average_depth, count(*) as total_earthquake from earthquakes
        where latitude between -5 and 5 group by country order by average_depth asc;
    """,

    "26. Countries having the highest ratio of shallow to deep earthquakes": """
        select place, sum(depth_km < 70) as shallow, sum(depth_km > 300) as deep,
        sum(depth_km < 70) / nullif(sum(depth_km > 300), 0) as ratio
        from earthquakes group by place order by ratio desc;
    """,

    "27. Average magnitude difference between earthquakes with tsunami without": """
        select round(avg(case when tsunami = 1 then mag end), 2) as avg_mag_with_alert,
        round(avg(case when tsunami = 0 then mag end), 2) as avg_mag_without_alert,
        round(avg(case when tsunami = 1 then mag end) - avg(case when tsunami = 0 then mag end), 2) as difference
        from earthquakes;
    """,

    "28. Events with the lowest data reliability (highest average error margins)": """
        select id, place, mag, gap, rms from earthquakes where gap is not null and rms is not null
        order by gap, rms desc;
    """,

    "30. Regions with the highest frequency of deep-focus earthquakes (depth > 300 km)": """
        select place as region, count(*) as deep_focus_quakes from earthquakes where depth_km > 300
        group by region order by deep_focus_quakes desc;
        """
}

st.title("Earthquake Data Analysis")
st.write("An analysis of all recorded earthquakes in the past 5 years")

# Dropdown
task = st.selectbox("Choose Query Number", list(queries.keys()))

# Run
if st.button("Run Query"):
    query = queries[task]
    df = pd.read_sql(query, engine)

    st.subheader(f"Results for : {task}")
    st.dataframe(df, use_container_width = True)

