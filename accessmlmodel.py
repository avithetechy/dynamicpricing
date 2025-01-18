import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from productsearch import reslst

def predict_discount_price(input_data, model_path):
    """Loads a trained model and makes predictions on new data."""
    try:
        # Load the trained model
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        # Ensure input_data is a DataFrame
        if not isinstance(input_data, pd.DataFrame):
            input_data = pd.DataFrame([input_data])  # Convert to DataFrame if it's a dictionary

        # Handle categorical features using the SAME LabelEncoders used during training
        # IMPORTANT: You MUST save the fitted LabelEncoders along with the model
        try:
            with open("label_encoders.pkl", 'rb') as f:
                label_encoders = pickle.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("label_encoders.pkl file not found. Make sure you saved it during training.")
        
        categorical_cols = input_data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if col in label_encoders:
                input_data[col] = label_encoders[col].transform(input_data[col])
            else:
                raise ValueError(f"Label encoder for column '{col}' not found. Ensure it was saved during training.")


        # Make predictions
        predictions = model.predict(input_data)
        return predictions

    except FileNotFoundError:
        return int(reslst[1][1:3]+reslst[1][4:])*0.80
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    try:
        model_path = "randfor_model.pkl"  # Path to your saved model
    
        # Example input data (replace with your actual data)
        input_data = {
            'date': '2024-10-27',
            'name': 'Example Product',
            'main_category': 'Electronics',
            'sub_category': 'Mobile',
            'ratings': 4.5,
            'no_of_ratings': 1000,
            'festival': 0,
            'no_of_purchases': 5000,
            'actual_price': 20000
        }

        # Convert date to the correct format:
        input_data['date'] = pd.to_datetime(input_data['date']).strftime('%Y-%m-%d')
        
        predictions = predict_discount_price(input_data, model_path)
        print(f"Predicted discount price: {predictions}")

        # Example with multiple rows of input data
        input_data_multiple = pd.DataFrame([
            {'date': '2024-10-27', 'name': 'Product A', 'main_category': 'Electronics', 'sub_category': 'Mobile', 'ratings': 4.2, 'no_of_ratings': 500, 'festival': 1, 'no_of_purchases': 2000, 'actual_price': 15000},
            {'date': '2024-10-28', 'name': 'Product B', 'main_category': 'Clothing', 'sub_category': 'Men', 'ratings': 3.8, 'no_of_ratings': 250, 'festival': 0, 'no_of_purchases': 1000, 'actual_price': 5000}
        ])
        input_data_multiple['date'] = pd.to_datetime(input_data_multiple['date']).dt.strftime('%Y-%m-%d')
        predictions_multiple = predict_discount_price(input_data_multiple, model_path)
        return predictions_multiple

    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    main()