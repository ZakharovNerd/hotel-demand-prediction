# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hotel demand prediction",
        page_icon="🏨",
    )

    st.write('# The first graph')

    st.write('### Exploring seasonality')
    
    hotel_demand = pd.read_csv('data/hotel_bookings.csv')
    hotel_demand['arrival_month_num'] = pd.to_datetime(hotel_demand.arrival_date_month, format='%B').dt.month
    hotel_demand['arrival_date'] = pd.to_datetime((hotel_demand['arrival_date_year'].map(str) + "-" + hotel_demand['arrival_month_num'].map(str) + "-" + hotel_demand['arrival_date_day_of_month'].map(str)),yearfirst=True)
    hotel_demand2 = hotel_demand.query("reservation_status not in ('No-Show','Canceled')")

    hotel_ts = hotel_demand2[['arrival_date', 'adults', 'children', 'babies']]

    hotel_ts.insert(loc=4,column='rooms', value=1)
    hotel_ts = hotel_ts.set_index('arrival_date').to_period('D')

    hotel_ts = hotel_ts.resample("D").sum()

    X = hotel_ts.copy()

    X["day"] = X.index.dayofweek
    X["week"] = X.index.week 
    X["dayofyear"] = X.index.dayofyear
    X["year"] = X.index.year
    X["month"] = X.index.month

    fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(11, 6))
    sns.lineplot(data=X, y="rooms", hue="week", x="day", ax=ax0)
    sns.lineplot(data=X, y="rooms", hue="year", x="dayofyear", ax=ax1)
    sns.lineplot(data=X, y="rooms", hue="year", x="month", ax=ax2)

    st.pyplot(fig)


if __name__ == "__main__":
    run()
