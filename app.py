from flask import Flask, jsonify, request, render_template
import pandas as pd

app = Flask(__name__)

def load_data():
    df = pd.read_csv("data/transactions.csv")

    df.columns = df.columns.str.replace("'", "", regex=False)

    df["TRADDATE"] = (
        df["TRADDATE"]
        .str.replace("'", "", regex=False)
    )

    # Convert to datetime
    df["TRADDATE"] = pd.to_datetime(df["TRADDATE"])

    # Clean text columns
    df["SCHEME"] = (
        df["SCHEME"]
        .str.replace("'", "", regex=False)
    )

    df["INV_NAME"] = (
        df["INV_NAME"]
        .str.replace("'", "", regex=False)
    )

    df["PAN"] = (
        df["PAN"]
        .str.replace("'", "", regex=False)
    )

    return df
def filter_by_date(df, start_date, end_date):

    if start_date:
        df = df[
            df["TRADDATE"] >=
            pd.to_datetime(start_date)
        ]

    if end_date:
        df = df[
            df["TRADDATE"] <=
            pd.to_datetime(end_date)
        ]

    return df

@app.route("/")
def home():
    return "Mutual Fund Dashboard Running"

@app.route("/api/mutual-fund-summary")
def mutual_fund_summary():

    df = load_data()
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    df = filter_by_date(
        df,
        start_date,
        end_date
    )

    summary = (
        df.groupby("SCHEME")
          .agg({
              "AMOUNT": "sum",
              "UNITS": "sum",
              "PURPRICE": "mean"
          })
          .reset_index()
    )

    return jsonify(summary.to_dict(orient="records"))

@app.route("/api/investor-fund-summary")
def investor_fund_summary():

    df = load_data()

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    df = filter_by_date(
        df,
        start_date,
        end_date
    )

    summary = (
        df.groupby(["INV_NAME", "SCHEME"])
        .agg({
            "AMOUNT": "sum",
            "UNITS": "sum"
        })
        .reset_index()
    )

    return jsonify(
        summary.to_dict(orient="records")
    )


@app.route("/api/investors")
def investors():

    df = load_data()

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    df = filter_by_date(
        df,
        start_date,
        end_date
    )

    summary = (
        df.groupby(["PAN", "INV_NAME"])
        .agg({
            "AMOUNT": "sum"
        })
        .reset_index()
    )

    return jsonify(
        summary.to_dict(orient="records")
    )


@app.route("/api/fund-purchase-summary")
def fund_purchase_summary():

    df = load_data()

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    df = filter_by_date(
        df,
        start_date,
        end_date
    )

    summary = (
        df.groupby("SCHEME")
        .agg({
            "AMOUNT": "sum",
            "UNITS": "sum"
        })
        .reset_index()
    )

    return jsonify(
        summary.to_dict(orient="records")
    )
@app.route("/dashboard")
def dashboard():
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)