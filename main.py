import streamlit as st
import numpy as np
import pandas as pd

# import local modules
from BSModel import BSModel, ImpliedVol

st.set_page_config(
    page_title="BS Option Pricer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "This is an option pricing tool developed by **Qing Shang**. It uses the Black-Scholes model to do the calculations and gives analytical results of implied volatility and the Greeks."
    }
)

# sidebar design
st.title('Black-Scholes Option Pricer')
st.sidebar.title('Black-Scholes Option Pricer')
st.sidebar.markdown(':grey[Author:]')
linkedin_logo = 'https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg'
st.sidebar.markdown(f'<img src={linkedin_logo} width="25" heigh="25">[**Qing Shang**](www.linkedin.com/in/qing-shang-columbia)',
                    unsafe_allow_html=True)
st.sidebar.header('Pricing Parameters')

# Input
S0 = st.sidebar.number_input(label = "Underlying Asset Price", min_value = 0.00, max_value = None, value = 90.00, step = 0.01)
K = st.sidebar.number_input(label = "Strike Price", min_value = 0.00, max_value = None, value = 100.00, step = 0.01)
T = st.sidebar.number_input(label = "Time to Maturity (in years)", min_value = 0.00, max_value = None, value = 2.00, step = 0.01)
r = st.sidebar.number_input(label = "Risk-free Rate (%)", min_value = 0.00, max_value = None, value = 5.00, step = 0.01) / 100
sigma = st.sidebar.number_input(label = "Volatility (%)", min_value = 0.00, max_value = None, value = 10.00, step = 0.01) / 100

st.sidebar.divider()

st.sidebar.header('Graphical Parameters')
st.sidebar.subheader('Spot Price') 
S_min = st.sidebar.number_input(label = "Min Spot Price", min_value = 0.00, max_value = None, value = 0.5 * S0, step = 0.01)
S_max = st.sidebar.number_input(label = "Max Spot Price", min_value = 0.00, max_value = None, value = 1.5 * S0, step = 0.01)

st.sidebar.subheader('Volatility')
vol_min = st.sidebar.number_input(label = "Min Volatility (%)", min_value = 0.00, max_value = None, value = 50 * sigma, step = 0.01) / 100
vol_max = st.sidebar.number_input(label = "Max Volatility (%)", min_value = 0.00, max_value = None, value = 150 * sigma, step = 0.01) / 100

st.sidebar.divider()

st.sidebar.header('Implied Volatility Parameters')
option_type = st.sidebar.selectbox(label = "Option Type", options = ['Call', 'Put'], index = 0)
mkt_price = st.sidebar.number_input(label = "Option Market Price", min_value = 0.00, max_value = None, value = 5.00, step = 0.01)
initial_guess = st.sidebar.number_input(label = "Initial Guess for Implied Volatility (%)", min_value = 0.00, max_value = None, value = 20.00, step = 0.01) / 100

# calculate the price
bs = BSModel(S0, K, T, r, sigma)
call_price = bs.bs_call()
put_price = bs.bs_put()

# data for the graph
df_spot = pd.DataFrame({'spot_price': np.linspace(S_min, S_max, 100),
'call': np.array([BSModel(s0, K, T, r, sigma).bs_call() for s0 in np.linspace(S_min, S_max, 100)]),
'put': np.array([BSModel(s0, K, T, r, sigma).bs_put() for s0 in np.linspace(S_min, S_max, 100)])})

df_vol = pd.DataFrame({'volatility': np.linspace(vol_min, vol_max, 100),
'call': np.array([BSModel(S0, K, T, r, vol).bs_call() for vol in np.linspace(vol_min, vol_max, 100)]),
'put': np.array([BSModel(S0, K, T, r, vol).bs_put() for vol in np.linspace(vol_min, vol_max, 100)])})

df_time = pd.DataFrame({'time': np.linspace(0, T, 100),
'call': np.array([BSModel(S0, K, t, r, sigma).bs_call() for t in np.linspace(0, T, 100)]),
'put': np.array([BSModel(S0, K, t, r, sigma).bs_put() for t in np.linspace(0, T, 100)])})

# calcualte the implied volatility
implied_vol = ImpliedVol(S0, K, T, r, mkt_price, option_type, initial_guess)
imp_vol = implied_vol.implied_vol()


# calculate the greeks
bs_imp = BSModel(S0, K, T, r, sigma)

call_delta = bs_imp.bs_call_delta()
put_delta = bs_imp.bs_put_delta()
df_call_delta = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_call_delta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_call_delta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_call_delta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_call_delta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_call_delta() for s0 in np.linspace(S_min, S_max, 100)])
})
df_put_delta = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_put_delta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_put_delta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_put_delta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_put_delta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_put_delta() for s0 in np.linspace(S_min, S_max, 100)])
})

gamma = bs_imp.bs_gamma()
df_gamma = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_gamma() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_gamma() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_gamma() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_gamma() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_gamma() for s0 in np.linspace(S_min, S_max, 100)])
})

call_theta = bs_imp.bs_call_theta()
put_theta = bs_imp.bs_put_theta()
df_call_theta = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_call_theta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_call_theta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_call_theta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_call_theta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_call_theta() for s0 in np.linspace(S_min, S_max, 100)])
})
df_put_theta = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_put_theta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_put_theta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_put_theta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_put_theta() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_put_theta() for s0 in np.linspace(S_min, S_max, 100)])                       
})

vega = bs_imp.bs_vega()
df_vega = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_vega() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_vega() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_vega() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_vega() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_vega() for s0 in np.linspace(S_min, S_max, 100)])
})

call_rho = bs_imp.bs_call_rho()
put_rho = bs_imp.bs_put_rho()
df_call_rho = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_call_rho() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_call_rho() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_call_rho() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_call_rho() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_call_rho() for s0 in np.linspace(S_min, S_max, 100)])
})
df_put_rho = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_put_rho() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_put_rho() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_put_rho() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_put_rho() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_put_rho() for s0 in np.linspace(S_min, S_max, 100)])
})

vanna = bs_imp.bs_vanna()
df_vanna = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_vanna() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_vanna() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_vanna() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_vanna() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_vanna() for s0 in np.linspace(S_min, S_max, 100)])
})

volga = bs_imp.bs_volga()
df_volga = pd.DataFrame({
    'Spot': np.linspace(S_min, S_max, 100),
    'vol=10%': np.array([BSModel(s0, K, T, r, 0.1).bs_volga() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=30%': np.array([BSModel(s0, K, T, r, 0.3).bs_volga() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=50%': np.array([BSModel(s0, K, T, r, 0.5).bs_volga() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=80%': np.array([BSModel(s0, K, T, r, 0.8).bs_volga() for s0 in np.linspace(S_min, S_max, 100)]),
    'vol=100%': np.array([BSModel(s0, K, T, r, 1.0).bs_volga() for s0 in np.linspace(S_min, S_max, 100)])
})


# display the results
tab1, tab2 = st.tabs(["Pricing", "Implied Volatility and Greeks"])

with tab1:
    st.subheader('Black-Scholes Pricing')
    st.write(f'**Pricing Parameters**')
    df_option_info = pd.DataFrame({'Spot Price': [S0], 
    'Strike Price': [K], 'Time to Maturity': [T], 'Risk-free Rate': [r], 'Volatility': [sigma]}, index = None)
    st.table(df_option_info)

    st.markdown(f'### :material/Payments: European Call Option Price: ${call_price: .2f}')
    st.markdown(f'### :material/Payments: European Put Option Price: ${put_price: .2f}')

    st.divider()

    st.write(f'### :material/analytics: Graphs')
    st.write(f'**Option Price vs. Spot Price**')
    st.line_chart(data = df_spot.set_index('spot_price'), x_label='Spot Price', y_label='Option Price', use_container_width=True)
    st.write(f'**Option Price vs. Volatility**')
    st.line_chart(data = df_vol.set_index('volatility'), x_label='Volatility', y_label='Option Price', use_container_width=True, color=['#017D6F', '#8AD088'])
    st.write(f'**Option Price vs. Time to Maturity**')
    st.line_chart(data = df_time.set_index('time'), x_label='Time to Maturity', y_label='Option Price', use_container_width=True, color=['rgb(231,098,084)', 'rgb(255,208,111)'])
    

with tab2:
    st.write(f'### :material/monitoring: Implied Volatility: {imp_vol*100:.2f}%')
    st.markdown(':blue-background[The implied volatility is solved by Newton\'s method.]')
    df_iv_info = pd.DataFrame({'Option Type': [option_type], 'Market Price': [mkt_price], 'Spot Price': [S0], 
    'Strike Price': [K], 'Time to Maturity': [T], 'Risk-free Rate': [r]}, index = None)
    st.table(df_iv_info)

    st.divider()

    st.write('### :material/calculate: Greeks')
    df_greek = pd.DataFrame({
        'Greek': ['Delta', 'Gamma', 'Theta', 'Vega', 'Rho', 'Vanna', 'Volga'],
        'Call': [call_delta, gamma, call_theta, vega, call_rho, vanna, volga],
        'Put': [put_delta, gamma, put_theta, vega, put_rho, vanna, volga]
    })
    st.markdown(':blue-background[The Greeks are calculated using the volatility entered in the sidebar, instead of the implied volatility.]')
    st.markdown(':blue-background[To get the Greeks based on the implied volatility, please input it through the sidebar\'s *Volatility* field.]')
    st.dataframe(data = df_greek.set_index('Greek'), use_container_width = True)
    
    st.write('**Delta vs. Spot Price**')
    row1 = st.columns(2)
    row1[0].markdown('''<div style="text-align: center;"> European Call </div>''', unsafe_allow_html=True)  # to center the text
    row1[0].line_chart(data = df_call_delta.set_index('Spot'), x_label='Spot Price', y_label='Delta', use_container_width=True)
    row1[1].markdown('''<div style="text-align: center;"> European Put </div>''', unsafe_allow_html=True)
    row1[1].line_chart(data = df_put_delta.set_index('Spot'), x_label='Spot Price', y_label='Delta', use_container_width=True)

    st.write('**Gamma vs. Spot Price**')
    st.line_chart(data = df_gamma.set_index('Spot'), x_label='Spot Price', y_label='Gamma', use_container_width=True)
    st.write('**Theta vs. Spot Price**')
    
    row2 = st.columns(2)
    row2[0].markdown('''<div style="text-align: center;"> European Call </div>''', unsafe_allow_html=True)
    row2[0].line_chart(data = df_call_theta.set_index('Spot'), x_label='Spot Price', y_label='Theta', use_container_width=True)
    row2[1].markdown('''<div style="text-align: center;"> European Put </div>''', unsafe_allow_html=True)
    row2[1].line_chart(data = df_put_theta.set_index('Spot'), x_label='Spot Price', y_label='Theta', use_container_width=True)

    st.write('**Vega vs. Spot Price**')
    st.line_chart(data = df_vega.set_index('Spot'), x_label='Spot Price', y_label='Vega', use_container_width=True)
    
    st.write('**Rho vs. Spot Price**')
    row3 = st.columns(2)
    row3[0].markdown('''<div style="text-align: center;"> European Call </div>''', unsafe_allow_html=True)
    row3[0].line_chart(data = df_call_rho.set_index('Spot'), x_label='Spot Price', y_label='Rho', use_container_width=True)
    row3[1].markdown('''<div style="text-align: center;"> European Put </div>''', unsafe_allow_html=True)
    row3[1].line_chart(data = df_put_rho.set_index('Spot'), x_label='Spot Price', y_label='Rho', use_container_width=True)

    st.write('**Vanna vs. Spot Price**')
    st.line_chart(data = df_vanna.set_index('Spot'), x_label='Spot Price', y_label='Vanna', use_container_width=True)
    
    st.write('**Volga vs. Spot Price**')
    st.line_chart(data = df_volga.set_index('Spot'), x_label='Spot Price', y_label='Volga', use_container_width=True)

