
# Risk Management Simulator

![App Image](./image.png)

## Overview

The Risk Management Simulator is a Streamlit-based application designed to simulate various risk/return scenarios. It allows users to adjust multiple parameters and visualize the potential outcomes of different risk management strategies.

**[Link to the app](https://risk-return-analysis.streamlit.app/)**

## Features

- **Trading Simulations**: Simulate trading outcomes over a year with customizable parameters such as win rate, number of trades per year, and risk per trade.
- **Interactive Charts**: Visualize average returns and win rates through interactive Plotly charts.

## Installation

To run the application locally, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/chrisduvillard/RiskSim.git
   cd RiskSim
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```sh
   streamlit run src/app.py
   ```

## Project Structure

```
risk-management-simulator/
│
├── src/
│   ├── app.py
│   ├── style.py
│   ├── risk_simulation.py
│
├── config/
│   ├── slider_configs.py
│   ├── __init__.py
│
├── venv/
│
├── requirements.txt
├── README.md
├── LICENSE.txt
|── image.png
|── image_1.png
└── image_2.png
```

## Usage

1. Adjust the simulation parameters using the sliders in the sidebar.
2. Click on "Run Simulation" to see the results.
3. Explore the results through the "RPUR Analysis" and "Win Rate Analysis" tabs.

## Example

### Simulation Parameters
- Number of Trades per Year: 30
- Win Rate: 40%
- Risk per Trade: 1%
- Return Per Unit Risk: 3x

### Visualization

Display the expected annualized return for different return per unit risk values.

![App Image](./image_1.png)

Display the expected annualized return for different win rates.

![App Image](./image_2.png)


## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any features, bug fixes, or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Author

Made with ❤️ by [Chris](https://github.com/chrisduvillard)

## Acknowledgments

- Streamlit
- Plotly

---

Feel free to reach out if you have any questions or need further assistance.
