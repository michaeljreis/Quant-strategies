import tkinter as tk
import yfinance as yf

def calculate_intrinsic_value():
    ticker = entry_ticker.get()
    options = yf.Ticker(ticker).options
    expiration_dates = list(options)

    var = tk.StringVar()
    var.set(expiration_dates[0])
    dropdown = tk.OptionMenu(root, var, *expiration_dates)
    dropdown.pack()

    def get_expiration():
        expiration = var.get()
        strike_price = float(entry_strike_price.get())
        option_type = var_option_type.get()
        stock_price = yf.download(ticker, period='1mo')["Adj Close"][-1]

        options = yf.Ticker(ticker).option_chain(expiration)
        calls = options.calls
        puts = options.puts
        calls['mid'] = (calls['bid'] + calls['ask']) / 2
        puts['mid'] = (puts['bid'] + puts['ask']) / 2

        if option_type == "Call":
            intrinsic_value = max(0, stock_price - strike_price)
            mid = calls['mid'].loc[calls['strike'] == strike_price]
            time_value = mid.iloc[0] - intrinsic_value
        else:
            intrinsic_value = max(0, strike_price - stock_price)
            mid = puts['mid'].loc[puts['strike'] == strike_price]
            time_value = mid.iloc[0] - intrinsic_value

        result_label.config(text=f"With {ticker} stock trading at ${stock_price:.2f}, the time value of the ${strike_price:.2f} strike {option_type} is ${time_value:.2f}")

    label_strike_price = tk.Label(root, text="Enter Strike Price:")
    label_strike_price.pack()

    entry_strike_price = tk.Entry(root)
    entry_strike_price.pack()

    label_option_type = tk.Label(root, text="Select Option Type:")
    label_option_type.pack()

    var_option_type = tk.StringVar()
    var_option_type.set("Call")
    option_type_radiobutton = tk.Radiobutton(root, text="Call", variable=var_option_type, value="Call")
    option_type_radiobutton.pack()
    option_type_radiobutton = tk.Radiobutton(root, text="Put", variable=var_option_type, value="Put")
    option_type_radiobutton.pack()

    calculate_button = tk.Button(root, text="Calculate", command=get_expiration)
    calculate_button.pack()

    result_label = tk.Label(root, text="")
    result_label.pack()

root = tk.Tk()
root.title('Intrinsic Value Calculator')
root.geometry("800x400")

label_ticker = tk.Label(root, text="Enter Stock Ticker:")
label_ticker.pack()

entry_ticker = tk.Entry(root)
entry_ticker.pack()

calculate_button = tk.Button(root, text="Get Options", command=calculate_intrinsic_value)
calculate_button.pack()

root.mainloop()
