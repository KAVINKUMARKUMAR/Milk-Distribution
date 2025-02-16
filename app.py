from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Function to calculate price per litre based on fat and snf
def calculate_price(fat, snf):
    base_price = 32.35
    fat_increase = (fat - 4.0) * 0.28 if fat > 4.0 else 0
    snf_increase = (snf - 8.0) * 0.28 if snf > 8.0 else 0
    return round(base_price + fat_increase + snf_increase, 2)

# Function to distribute litres among 18 members
def distribute_litres(total_litre):
    members = 18
    min_litre, max_litre = 8, 40
    litres = [random.uniform(min_litre, max_litre) for _ in range(members)]
    
    # Adjust litres to match total
    scale_factor = total_litre / sum(litres)
    litres = [round(l * scale_factor, 2) for l in litres]
    
    # Final adjustment
    litres[-1] += round(total_litre - sum(litres), 2)
    return litres

# Function to distribute fat and snf
def distribute_fat_snf():
    members = 18
    fat_values = [4.0, 4.1, 4.2]
    snf_values = [8.0, 8.1, 8.2]

    fat_list = [random.choice(fat_values) for _ in range(members)]
    snf_list = [random.choice(snf_values) for _ in range(members)]
    
    return fat_list, snf_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    total_litre = float(data['total_litre'])
    total_amount = float(data['total_amount'])

    litres = distribute_litres(total_litre)
    fat_list, snf_list = distribute_fat_snf()
    
    prices = [calculate_price(fat_list[i], snf_list[i]) for i in range(18)]
    amounts = [round(litres[i] * prices[i], 2) for i in range(18)]
    
    # Adjusting total amount to match user input
    scale_factor = total_amount / sum(amounts)
    amounts = [round(a * scale_factor, 2) for a in amounts]
    amounts[-1] += round(total_amount - sum(amounts), 2)

    # Round amount calculation
    round_amounts = [round(a) for a in amounts]
    round_amounts[-1] += round(total_amount - sum(round_amounts), 2)

    result = {
        "members": [
            {
                "id": i+1,
                "litres": litres[i],
                "fat": fat_list[i],
                "snf": snf_list[i],
                "price_per_litre": prices[i],
                "amount": amounts[i],
                "round_amount": round_amounts[i]
            }
            for i in range(18)
        ],
        "totals": {
            "total_litres": sum(litres),
            "total_amount": sum(amounts),
            "total_round_amount": sum(round_amounts)
        }
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)