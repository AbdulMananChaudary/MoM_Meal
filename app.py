from flask import Flask, render_template_string, jsonify, request
import random
from datetime import datetime
import os

app = Flask(__name__)

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Recipe database - Authentic Pakistani meals for moms
recipes = [
    # Breakfast - Quick weekday options
    {
        "name": "Chai Paratha Nashta", 
        "ingredients": ["wheat flour", "ghee", "salt", "chai patti"],
        "type": "breakfast",
        "tip": "Roll it thin and crispy - perfect with ginger tea! Jo bhi ho, breakfast mein paratha toh banta hai"
    },
    {
        "name": "Khagina (Anda Bhurji)", 
        "ingredients": ["eggs", "onion", "tomato", "green chili"],
        "type": "breakfast",
        "tip": "Don't overcook! Thora sa namm rakho - kids love it with ketchup"
    },
    {
        "name": "Aloo Paratha", 
        "ingredients": ["potato", "wheat flour", "spices", "coriander"],
        "type": "breakfast",
        "tip": "Make extra parathas! Wrap in foil - perfect for lunch boxes. Bachon ka favorite"
    },
    {
        "name": "Halwa Puri", 
        "ingredients": ["semolina", "flour", "sugar", "ghee"],
        "type": "breakfast",
        "tip": "Sunday special! Whole family will wake up smiling. Mehnat hai but dil khush ho jata hai"
    },
    {
        "name": "Anda Bread Omelette", 
        "ingredients": ["bread", "eggs", "green chili", "butter"],
        "type": "breakfast",
        "tip": "10 minute breakfast when you're running late! School jaane se pehle quick and filling"
    },
    {
        "name": "Anda Paratha", 
        "ingredients": ["eggs", "wheat flour", "onion", "green chili"],
        "type": "breakfast",
        "tip": "Kids absolutely love this! Fold the egg inside while hot"
    },
    
    # Lunch - Main hearty meals
    {
        "name": "Chicken Karahi", 
        "ingredients": ["chicken", "tomato", "ginger", "green chili"],
        "type": "lunch",
        "tip": "Dum lagao for 5 mins - the smell will call everyone to the table! Husband ka favorite"
    },
    {
        "name": "Simple Chicken Biryani", 
        "ingredients": ["chicken", "rice", "yogurt", "biryani masala"],
        "type": "lunch",
        "tip": "Friday special! Make raita on the side. Bachay khud hi mang kar khayenge"
    },
    {
        "name": "Aloo Qeema", 
        "ingredients": ["minced meat", "potato", "onion", "tomato"],
        "type": "lunch",
        "tip": "Budget-friendly and filling! With warm roti - no one stays hungry"
    },
    {
        "name": "Daal Makhani", 
        "ingredients": ["black lentils", "cream", "butter", "spices"],
        "type": "lunch",
        "tip": "Slow cook karo - rich and creamy banti hai. Achay restaurants se bhi better"
    },
    {
        "name": "Chicken Tikka Masala", 
        "ingredients": ["chicken", "yogurt", "cream", "tikka spices"],
        "type": "lunch",
        "tip": "Overnight marination ka kamaal! Tender and juicy. Guests bhi impress ho jayenge"
    },
    {
        "name": "Palak Paneer", 
        "ingredients": ["spinach", "paneer", "cream", "onion"],
        "type": "lunch",
        "tip": "Sabzi bhi hai, protein bhi! Bachon ko greens khilane ka secret weapon"
    },
    {
        "name": "Mutton Korma", 
        "ingredients": ["mutton", "yogurt", "fried onions", "whole spices"],
        "type": "lunch",
        "tip": "Special occasions ke liye perfect! Pyaaz achai tarah bhuno - that's the secret"
    },
    {
        "name": "Chicken Pulao", 
        "ingredients": ["chicken", "rice", "yogurt", "whole spices"],
        "type": "lunch",
        "tip": "Easier than biryani, just as delicious! One pot meal - less dishes to wash"
    },
    
    # Dinner - Lighter comfort meals
    {
        "name": "Daal Chawal", 
        "ingredients": ["lentils", "rice", "onion", "garlic"],
        "type": "dinner",
        "tip": "Sab ki comfort food! Thakawat dur kar de. Lemon squeeze with salad - perfect"
    },
    {
        "name": "Creamy Chicken Macaroni", 
        "ingredients": ["macaroni", "chicken", "cream", "cheese"],
        "type": "dinner",
        "tip": "Bachon ka all-time favorite! Quick banti hai, sab khush. Extra cheese daal do"
    },
    {
        "name": "Seekh Kabab with Roti", 
        "ingredients": ["minced meat", "spices", "coriander", "onion"],
        "type": "dinner",
        "tip": "Oven mein bana lo - healthy! Green chutney with raita - restaurant style dinner"
    },
    {
        "name": "Mix Vegetable Curry", 
        "ingredients": ["potato", "carrot", "peas", "cauliflower"],
        "type": "dinner",
        "tip": "Light dinner after heavy lunch! Colorful vegetables - eyes aur dil dono khush"
    },
    {
        "name": "Aloo Palak", 
        "ingredients": ["spinach", "potato", "garlic", "spices"],
        "type": "dinner",
        "tip": "Healthy aur tasty dono! Roti ke saath perfect. Iron bhi, taste bhi"
    },
    {
        "name": "Chicken Yakhni Soup", 
        "ingredients": ["chicken", "vegetables", "rice", "spices"],
        "type": "dinner",
        "tip": "Light dinner ya bimari mein best! Ghar ki healing in a bowl"
    },
    {
        "name": "Daal Mash", 
        "ingredients": ["urad lentils", "onion", "garlic", "butter"],
        "type": "dinner",
        "tip": "Simple, healthy, comforting. With tandoori roti - perfect simple dinner"
    },
    
    # Dessert
    {
        "name": "Gajar Ka Halwa", 
        "ingredients": ["carrot", "milk", "sugar", "khoya"],
        "type": "dessert",
        "tip": "Winter special! Garam garam with cream or ice cream. Dil aur ghar dono warm"
    },
    {
        "name": "Kheer (Rice Pudding)", 
        "ingredients": ["rice", "milk", "sugar", "cardamom"],
        "type": "dessert",
        "tip": "Kisi bhi khushi pe banti hai! Stirring mein time lagta hai but worth it"
    },
    {
        "name": "Falooda", 
        "ingredients": ["vermicelli", "basil seeds", "milk", "ice cream"],
        "type": "dessert",
        "tip": "Garmi mein instant happiness! Bachay pagal ho jate hain. Summer treat"
    }
]

# Main HTML template
html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aaj Ki Pakayein - Daily Meal Planner</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Nunito', sans-serif;
            background: #FFF9F0;
            color: #4A4A4A;
            line-height: 1.6;
            min-height: 100vh;
            padding: 15px;
        }
        
        .container {
            max-width: 1100px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 25px;
            padding: 15px 0;
        }
        
        h1 {
            color: #E57C23;
            font-size: 2.2rem;
            margin-bottom: 5px;
            font-weight: 700;
        }
        
        .subtitle {
            font-size: 1rem;
            color: #666;
            margin-bottom: 15px;
        }

        .top-actions {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }

        .action-btn {
            background: white;
            color: #4A4A4A;
            border: 2px solid #E57C23;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }

        .action-btn:hover {
            background: #E57C23;
            color: white;
        }
        
        .welcome-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        
        .welcome-text {
            font-size: 1.1rem;
            margin-bottom: 20px;
            color: #4A4A4A;
            text-align: center;
        }

        .filter-section {
            background: #FFF9F0;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #FFE6CC;
        }

        .filter-title {
            font-size: 1rem;
            color: #4A4A4A;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .ingredient-filter {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #E5E5E5;
            border-radius: 8px;
            font-family: 'Nunito', sans-serif;
            font-size: 0.95rem;
            margin-bottom: 15px;
        }

        .ingredient-filter:focus {
            outline: none;
            border-color: #E57C23;
        }

        .meal-type-filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: center;
        }

        .filter-btn {
            background: white;
            border: 2px solid #E5E5E5;
            color: #4A4A4A;
            padding: 8px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }

        .filter-btn:hover, .filter-btn.active {
            background: #E57C23;
            color: white;
            border-color: #E57C23;
        }

        .button-group {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .suggest-btn {
            background: #E57C23;
            color: white;
            border: none;
            padding: 15px 35px;
            font-size: 1.1rem;
            border-radius: 8px;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
            font-weight: 700;
            transition: all 0.3s ease;
        }
        
        .suggest-btn:hover {
            background: #D16B1A;
            transform: translateY(-2px);
        }

        .surprise-btn {
            background: #9C27B0;
        }

        .surprise-btn:hover {
            background: #7B1FA2;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            display: none;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid #FFE6CC;
            border-top: 3px solid #E57C23;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .section-header {
            background: #E57C23;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            margin: 25px 0 15px 0;
            font-weight: 700;
            font-size: 1.1rem;
        }
        
        .meals-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .meal-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
            border: 1px solid #F0F0F0;
        }
        
        .meal-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        
        .meal-name {
            color: #E57C23;
            font-size: 1.2rem;
            margin-bottom: 12px;
            font-weight: 700;
            padding-right: 40px;
        }

        .save-btn {
            position: absolute;
            top: 15px;
            right: 15px;
            background: white;
            border: 2px solid #E57C23;
            color: #E57C23;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.3s ease;
            font-family: 'Nunito', sans-serif;
        }

        .save-btn:hover, .save-btn.saved {
            background: #E57C23;
            color: white;
        }
        
        .ingredients {
            margin-bottom: 15px;
        }
        
        .ingredient-item {
            background: #FFF9F0;
            padding: 6px 12px;
            border-radius: 6px;
            display: inline-block;
            margin: 4px 4px 4px 0;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid #FFE6CC;
            color: #666;
        }
        
        .tip {
            background: #FFF9F0;
            color: #4A4A4A;
            padding: 12px;
            border-radius: 8px;
            font-style: italic;
            margin: 15px 0;
            border-left: 3px solid #E57C23;
            font-size: 0.9rem;
        }
        
        .cook-btn {
            background: #E57C23;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
            font-size: 0.95rem;
            margin-top: 10px;
        }
        
        .cook-btn:hover {
            background: #D16B1A;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
        }

        .modal-content {
            background: white;
            margin: 5% auto;
            padding: 30px;
            border-radius: 12px;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #F0F0F0;
        }

        .modal-title {
            color: #E57C23;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0;
        }

        .close {
            font-size: 2rem;
            font-weight: bold;
            color: #999;
            cursor: pointer;
            transition: color 0.3s;
            background: none;
            border: none;
            line-height: 1;
        }

        .close:hover {
            color: #E57C23;
        }

        .saved-meal-item, .shopping-list-item {
            background: #FFF9F0;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 3px solid #E57C23;
        }

        .saved-meal-item h4 {
            color: #E57C23;
            margin-bottom: 8px;
            font-size: 1.1rem;
        }

        .shopping-list-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .add-ingredient-section {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #F0F0F0;
        }

        .add-ingredient-input {
            width: 70%;
            padding: 10px;
            border: 2px solid #E5E5E5;
            border-radius: 6px;
            font-family: 'Nunito', sans-serif;
            margin-right: 10px;
        }

        .add-ingredient-btn {
            background: #E57C23;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
        }

        .remove-btn {
            background: #f44336;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .clear-list-btn {
            background: #E57C23;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
            margin-top: 20px;
            width: 100%;
        }

        /* Feedback Button */
        .feedback-float-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 30px;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
            font-weight: 700;
            font-size: 1rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            z-index: 900;
            transition: all 0.3s ease;
        }

        .feedback-float-btn:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.4);
        }

        .feedback-form {
            margin-top: 20px;
        }

        .feedback-textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #E5E5E5;
            border-radius: 8px;
            font-family: 'Nunito', sans-serif;
            font-size: 0.95rem;
            margin-bottom: 15px;
            min-height: 100px;
            resize: vertical;
        }

        .rating-section {
            margin-bottom: 15px;
        }

        .rating-btn {
            background: white;
            border: 2px solid #E5E5E5;
            color: #4A4A4A;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
            margin-right: 8px;
            transition: all 0.3s ease;
        }

        .rating-btn:hover, .rating-btn.selected {
            background: #4CAF50;
            color: white;
            border-color: #4CAF50;
        }

        .submit-feedback-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-family: 'Nunito', sans-serif;
            font-weight: 600;
            width: 100%;
        }

        .surprise-overlay {
            display: none;
            position: fixed;
            z-index: 2000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #9C27B0 0%, #E57C23 100%);
        }

        .surprise-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: white;
            width: 90%;
            max-width: 600px;
        }

        .surprise-meal {
            background: white;
            padding: 35px;
            border-radius: 15px;
            color: #4A4A4A;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }

        .surprise-close-btn {
            background: white;
            color: #9C27B0;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 700;
            margin-top: 20px;
            font-family: 'Nunito', sans-serif;
        }

        .empty-state {
            text-align: center;
            padding: 40px 20px;
            color: #999;
        }
        
        footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px 0;
            color: #999;
            font-size: 0.9rem;
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 1.8rem;
            }
            
            .meals-container {
                grid-template-columns: 1fr;
            }
            
            .suggest-btn {
                padding: 14px 30px;
                font-size: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Aaj Ki Pakayein</h1>
            <p class="subtitle">Your daily meal planning companion</p>
            <div style="background: #FFF3CD; border: 1px solid #FFE69C; padding: 8px 15px; border-radius: 8px; margin-top: 10px; font-size: 0.85rem; color: #856404;">
                📌 <strong>Test Version:</strong> This is a test version. Your data stays on this device only. Full version will have cloud sync!
            </div>
        </header>

        <div class="top-actions">
            <button class="action-btn" onclick="showSavedMeals()">
                Saved Recipes (<span id="savedCount">0</span>)
            </button>
            <button class="action-btn" onclick="showShoppingList()">
                Shopping List (<span id="listCount">0</span>)
            </button>
        </div>
        
        <div class="welcome-card">
            <p class="welcome-text">Assalam-o-Alaikum! Plan your complete day with breakfast, lunch, and dinner suggestions</p>
            
            <div class="filter-section">
                <div class="filter-title">What ingredients do you have?</div>
                <input 
                    type="text" 
                    id="ingredientFilter" 
                    class="ingredient-filter" 
                    placeholder="Type ingredients: chicken, tomato, potato, onion..."
                >
                
                <div class="filter-title" style="margin-top: 15px;">Filter by meal type:</div>
                <div class="meal-type-filters">
                    <button class="filter-btn active" data-type="all" onclick="filterByType('all')">All</button>
                    <button class="filter-btn" data-type="breakfast" onclick="filterByType('breakfast')">Breakfast</button>
                    <button class="filter-btn" data-type="lunch" onclick="filterByType('lunch')">Lunch</button>
                    <button class="filter-btn" data-type="dinner" onclick="filterByType('dinner')">Dinner</button>
                    <button class="filter-btn" data-type="dessert" onclick="filterByType('dessert')">Dessert</button>
                </div>
            </div>

            <div class="button-group">
                <button class="suggest-btn" onclick="getMealSuggestions()">
                    Get Today's Meal Plan
                </button>
                <button class="suggest-btn surprise-btn" onclick="surpriseMe()">
                    Surprise Me!
                </button>
            </div>
        </div>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Finding the best recipes for you...</p>
        </div>
        
        <div id="mealsDisplay"></div>
        
        <!-- Saved Meals Modal -->
        <div id="savedMealsModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">Your Saved Recipes</h2>
                    <button class="close" onclick="closeModal('savedMealsModal')">&times;</button>
                </div>
                <div id="savedMealsList"></div>
            </div>
        </div>

        <!-- Shopping List Modal -->
        <div id="shoppingListModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">Shopping List</h2>
                    <button class="close" onclick="closeModal('shoppingListModal')">&times;</button>
                </div>
                <div id="shoppingListContent"></div>
                <div class="add-ingredient-section">
                    <p style="margin-bottom: 10px; font-weight: 600; color: #4A4A4A;">Add ingredient manually:</p>
                    <input type="text" id="manualIngredient" class="add-ingredient-input" placeholder="Enter ingredient name...">
                    <button class="add-ingredient-btn" onclick="addManualIngredient()">Add</button>
                </div>
                <button class="clear-list-btn" onclick="clearShoppingList()">Clear All Items</button>
            </div>
        </div>

        <!-- Surprise Mode Overlay -->
        <div id="surpriseOverlay" class="surprise-overlay">
            <div class="surprise-content">
                <div class="surprise-meal" id="surpriseMealContent"></div>
                <button class="surprise-close-btn" onclick="closeSurprise()">Let's Cook This!</button>
            </div>
        </div>

        <!-- Feedback Modal -->
        <div id="feedbackModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 class="modal-title">Share Your Feedback</h2>
                    <button class="close" onclick="closeModal('feedbackModal')">&times;</button>
                </div>
                <div class="feedback-form">
                    <p style="margin-bottom: 15px; color: #4A4A4A;">Your honest feedback helps us improve! Tell us what you think:</p>
                    
                    <div class="rating-section">
                        <p style="font-weight: 600; margin-bottom: 10px; color: #4A4A4A;">How would you rate this app?</p>
                        <button class="rating-btn" onclick="selectRating('love-it', this)">Love it! ❤️</button>
                        <button class="rating-btn" onclick="selectRating('good', this)">Good 👍</button>
                        <button class="rating-btn" onclick="selectRating('okay', this)">Okay 😐</button>
                        <button class="rating-btn" onclick="selectRating('not-great', this)">Not Great 👎</button>
                    </div>

                    <textarea 
                        id="feedbackText" 
                        class="feedback-textarea" 
                        placeholder="What do you like? What can we improve? Any features you wish we had?"
                    ></textarea>

                    <button class="submit-feedback-btn" onclick="submitFeedback()">Submit Feedback</button>
                </div>
            </div>
        </div>

        <!-- Floating Feedback Button -->
        <button class="feedback-float-btn" onclick="showFeedbackModal()">
            Give Feedback
        </button>
        
        <footer>
            <p>Made with care by Soviotech | Aaj Ki Pakayein &copy; 2025</p>
        </footer>
    </div>

    <script>
        let allRecipes = [];
        let currentFilter = 'all';
        let allMealsData = {};
        let currentSurpriseMeal = null;
        let selectedRating = null;

        // Generate or retrieve user ID for tracking
        let userId = localStorage.getItem('userId');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('userId', userId);
        }

        // Tracking function
        function trackEvent(eventName, extraData = '') {
            const fullEvent = extraData ? `${eventName}_${extraData}` : eventName;
            fetch(`/log_event?event=${encodeURIComponent(fullEvent)}&user_id=${userId}`)
                .catch(err => console.log('Tracking error:', err));
        }

        // Track page load
        trackEvent('page_loaded');

        updateSavedCount();
        updateShoppingListCount();

        function getMealSuggestions() {
            trackEvent('clicked_get_meal_plan');
            document.getElementById('loading').style.display = 'block';
            document.getElementById('mealsDisplay').innerHTML = '';
            
            fetch('/suggest')
                .then(response => response.json())
                .then(data => {
                    trackEvent('meal_plan_loaded');
                    allRecipes = data.all_meals || [];
                    allRecipes.forEach(meal => {
                        allMealsData[meal.name] = meal;
                    });
                    
                    document.getElementById('loading').style.display = 'none';
                    displayMealsByCategory(data);
                })
                .catch(error => {
                    console.error('Error:', error);
                    trackEvent('error_loading_meals');
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('mealsDisplay').innerHTML = 
                        '<div class="empty-state">Something went wrong. Please try again!</div>';
                });
        }
        
        function displayMealsByCategory(data) {
            const display = document.getElementById('mealsDisplay');
            display.innerHTML = '';

            if (data.breakfast && data.breakfast.length > 0) {
                display.innerHTML += '<div class="section-header">Breakfast</div>';
                const breakfastContainer = document.createElement('div');
                breakfastContainer.className = 'meals-container';
                data.breakfast.forEach(meal => {
                    breakfastContainer.appendChild(createMealCard(meal));
                });
                display.appendChild(breakfastContainer);
            }

            if (data.lunch && data.lunch.length > 0) {
                display.innerHTML += '<div class="section-header">Lunch</div>';
                const lunchContainer = document.createElement('div');
                lunchContainer.className = 'meals-container';
                data.lunch.forEach(meal => {
                    lunchContainer.appendChild(createMealCard(meal));
                });
                display.appendChild(lunchContainer);
            }

            if (data.dinner && data.dinner.length > 0) {
                display.innerHTML += '<div class="section-header">Dinner</div>';
                const dinnerContainer = document.createElement('div');
                dinnerContainer.className = 'meals-container';
                data.dinner.forEach(meal => {
                    dinnerContainer.appendChild(createMealCard(meal));
                });
                display.appendChild(dinnerContainer);
            }
        }

        function createMealCard(meal) {
            const isSaved = isMealSaved(meal.name);
            const card = document.createElement('div');
            card.className = 'meal-card';
            
            card.innerHTML = `
                <button class="save-btn ${isSaved ? 'saved' : ''}" onclick="saveMeal('${escapeHtml(meal.name)}', this)">
                    ${isSaved ? 'Saved' : 'Save'}
                </button>
                <h3 class="meal-name">${meal.name}</h3>
                <div class="ingredients">
                    ${meal.ingredients.map(ing => 
                        `<span class="ingredient-item">${ing}</span>`
                    ).join('')}
                </div>
                <div class="tip">${meal.tip}</div>
                <button class="cook-btn" onclick="selectMeal('${escapeHtml(meal.name)}')">
                    Cook This Meal
                </button>
            `;
            
            return card;
        }

        function displayFilteredMeals(meals) {
            const display = document.getElementById('mealsDisplay');
            display.innerHTML = '';
            
            if (meals.length === 0) {
                display.innerHTML = '<div class="empty-state">No recipes found with those ingredients. Try different ones!</div>';
                return;
            }

            const container = document.createElement('div');
            container.className = 'meals-container';
            meals.forEach(meal => {
                container.appendChild(createMealCard(meal));
            });
            display.appendChild(container);
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function saveMeal(mealName, button) {
            let saved = JSON.parse(localStorage.getItem('savedMeals') || '[]');
            const meal = allRecipes.find(m => m.name === mealName) || allMealsData[mealName];
            
            if (!meal) return;

            const index = saved.findIndex(m => m.name === mealName);
            
            if (index > -1) {
                saved.splice(index, 1);
                button.classList.remove('saved');
                button.textContent = 'Save';
                trackEvent('unsaved_recipe', mealName);
            } else {
                saved.push(meal);
                button.classList.add('saved');
                button.textContent = 'Saved';
                trackEvent('saved_recipe', mealName);
            }
            
            localStorage.setItem('savedMeals', JSON.stringify(saved));
            updateSavedCount();
        }

        function isMealSaved(mealName) {
            const saved = JSON.parse(localStorage.getItem('savedMeals') || '[]');
            return saved.some(m => m.name === mealName);
        }

        function updateSavedCount() {
            const saved = JSON.parse(localStorage.getItem('savedMeals') || '[]');
            document.getElementById('savedCount').textContent = saved.length;
        }

        function showSavedMeals() {
            trackEvent('viewed_saved_meals');
            const saved = JSON.parse(localStorage.getItem('savedMeals') || '[]');
            const list = document.getElementById('savedMealsList');
            
            if (saved.length === 0) {
                list.innerHTML = '<div class="empty-state">No saved recipes yet! Start saving your favorites!</div>';
            } else {
                list.innerHTML = saved.map(meal => `
                    <div class="saved-meal-item">
                        <h4>${meal.name}</h4>
                        <p><strong>Ingredients:</strong> ${meal.ingredients.join(', ')}</p>
                        <p style="font-style: italic; margin-top: 8px;">${meal.tip}</p>
                        <button class="remove-btn" onclick="removeSavedMeal('${escapeHtml(meal.name)}')">Remove</button>
                    </div>
                `).join('');
            }
            
            document.getElementById('savedMealsModal').style.display = 'block';
        }

        function removeSavedMeal(mealName) {
            let saved = JSON.parse(localStorage.getItem('savedMeals') || '[]');
            saved = saved.filter(m => m.name !== mealName);
            localStorage.setItem('savedMeals', JSON.stringify(saved));
            updateSavedCount();
            showSavedMeals();
        }

        function filterByIngredients() {
            const input = document.getElementById('ingredientFilter').value.toLowerCase().trim();
            
            if (!input) {
                if (allRecipes.length > 0) {
                    displayFilteredMeals(allRecipes);
                }
                return;
            }

            trackEvent('used_ingredient_filter', input);

            if (allRecipes.length === 0) {
                fetch('/all_recipes')
                    .then(response => response.json())
                    .then(recipes => {
                        allRecipes = recipes;
                        recipes.forEach(meal => {
                            allMealsData[meal.name] = meal;
                        });
                        performFilter(input);
                    });
            } else {
                performFilter(input);
            }
        }

        function performFilter(input) {
            const keywords = input.split(',').map(k => k.trim()).filter(k => k);
            
            let filtered = allRecipes.filter(meal => {
                return keywords.some(keyword => 
                    meal.ingredients.some(ing => ing.toLowerCase().includes(keyword))
                );
            });

            if (currentFilter !== 'all') {
                filtered = filtered.filter(m => m.type === currentFilter);
                // Limit to 2 when specific type is selected (randomized)
                if (filtered.length > 2) {
                    filtered = filtered.sort(() => Math.random() - 0.5).slice(0, 2);
                }
            }

            displayFilteredMeals(filtered);
        }

        function filterByType(type) {
            trackEvent('used_meal_type_filter', type);
            currentFilter = type;
            
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');

            if (allRecipes.length === 0) {
                fetch('/all_recipes')
                    .then(response => response.json())
                    .then(recipes => {
                        allRecipes = recipes;
                        recipes.forEach(meal => {
                            allMealsData[meal.name] = meal;
                        });
                        applyTypeFilter(type);
                    });
            } else {
                applyTypeFilter(type);
            }
        }

        function applyTypeFilter(type) {
            const input = document.getElementById('ingredientFilter').value.toLowerCase().trim();
            let filtered = type === 'all' ? allRecipes : allRecipes.filter(m => m.type === type);

            if (input) {
                const keywords = input.split(',').map(k => k.trim()).filter(k => k);
                filtered = filtered.filter(meal => {
                    return keywords.some(keyword => 
                        meal.ingredients.some(ing => ing.toLowerCase().includes(keyword))
                    );
                });
            }

            // Limit to maximum 2 recipes when filtering by specific type (randomized)
            if (type !== 'all' && filtered.length > 2) {
                filtered = filtered.sort(() => Math.random() - 0.5).slice(0, 2);
            }

            displayFilteredMeals(filtered);
        }

        function surpriseMe() {
            trackEvent('clicked_surprise_me');
            fetch('/all_recipes')
                .then(response => response.json())
                .then(meals => {
                    const randomMeal = meals[Math.floor(Math.random() * meals.length)];
                    allMealsData[randomMeal.name] = randomMeal;
                    trackEvent('surprise_showed', randomMeal.name);
                    showSurpriseMeal(randomMeal);
                });
        }

        function showSurpriseMeal(meal) {
            currentSurpriseMeal = meal;
            const content = document.getElementById('surpriseMealContent');
            content.innerHTML = `
                <h2 style="font-size: 2rem; margin-bottom: 20px; color: #E57C23;">${meal.name}</h2>
                <div style="margin: 20px 0;">
                    <strong style="font-size: 1.1rem;">Ingredients:</strong><br>
                    ${meal.ingredients.map(ing => `<span style="display: inline-block; background: #FFF9F0; padding: 5px 10px; margin: 5px; border-radius: 6px; border: 1px solid #FFE6CC;">${ing}</span>`).join('')}
                </div>
                <div style="background: #FFF9F0; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 3px solid #E57C23;">
                    <strong>Tip:</strong> ${meal.tip}
                </div>
            `;
            document.getElementById('surpriseOverlay').style.display = 'block';
        }

        function closeSurprise() {
            if (currentSurpriseMeal) {
                if (confirm('Add ingredients for "' + currentSurpriseMeal.name + '" to shopping list?')) {
                    addToShoppingList(currentSurpriseMeal.ingredients);
                    
                    // Ask if they want to save the recipe too
                    if (confirm('Would you also like to save this recipe?')) {
                        let saved = JSON.parse(localStorage.getItem('savedMeals') || '[]');
                        if (!saved.some(m => m.name === currentSurpriseMeal.name)) {
                            saved.push(currentSurpriseMeal);
                            localStorage.setItem('savedMeals', JSON.stringify(saved));
                            updateSavedCount();
                        }
                        alert('Recipe saved and ingredients added to shopping list!');
                    } else {
                        alert('Ingredients added to shopping list!');
                    }
                }
            }
            document.getElementById('surpriseOverlay').style.display = 'none';
            currentSurpriseMeal = null;
        }

        function selectMeal(mealName) {
            trackEvent('clicked_cook_meal', mealName);
            const meal = allRecipes.find(m => m.name === mealName) || allMealsData[mealName];
            
            if (!meal) {
                alert('Great choice! Happy cooking!');
                return;
            }
            
            if (confirm('Add ingredients for "' + mealName + '" to shopping list?')) {
                addToShoppingList(meal.ingredients);
                trackEvent('added_to_shopping_list', mealName);
                alert('Ingredients added to your shopping list!');
            } else {
                alert('Great choice! Happy cooking!');
            }
        }

        function addToShoppingList(ingredients) {
            let list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
            ingredients.forEach(ing => {
                if (!list.includes(ing)) {
                    list.push(ing);
                }
            });
            localStorage.setItem('shoppingList', JSON.stringify(list));
            updateShoppingListCount();
        }

        function showShoppingList() {
            trackEvent('viewed_shopping_list');
            const list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
            const content = document.getElementById('shoppingListContent');
            
            if (list.length === 0) {
                content.innerHTML = '<div class="empty-state">Your shopping list is empty! Add ingredients from meals or manually below.</div>';
            } else {
                content.innerHTML = list.map((item, index) => `
                    <div class="shopping-list-item">
                        <span><strong>${item}</strong></span>
                        <button class="remove-btn" onclick="removeFromList(${index})">Remove</button>
                    </div>
                `).join('');
            }
            
            document.getElementById('shoppingListModal').style.display = 'block';
        }

        // Feedback Functions
        function showFeedbackModal() {
            trackEvent('opened_feedback_modal');
            document.getElementById('feedbackModal').style.display = 'block';
        }

        function selectRating(rating, button) {
            selectedRating = rating;
            document.querySelectorAll('.rating-btn').forEach(btn => {
                btn.classList.remove('selected');
            });
            button.classList.add('selected');
            trackEvent('selected_rating', rating);
        }

        function submitFeedback() {
            const feedbackText = document.getElementById('feedbackText').value.trim();
            
            if (!selectedRating && !feedbackText) {
                alert('Please select a rating or provide feedback!');
                return;
            }

            const feedbackData = {
                feedback: feedbackText,
                rating: selectedRating || 'not_provided',
                user_id: userId
            };

            fetch('/submit_feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(feedbackData)
            })
            .then(response => response.json())
            .then(data => {
                trackEvent('submitted_feedback');
                alert('Thank you for your feedback! It helps us improve.');
                closeModal('feedbackModal');
                document.getElementById('feedbackText').value = '';
                selectedRating = null;
                document.querySelectorAll('.rating-btn').forEach(btn => {
                    btn.classList.remove('selected');
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Sorry, there was an error submitting your feedback. Please try again.');
            });
        }

        function addManualIngredient() {
            trackEvent('added_manual_ingredient');
            const input = document.getElementById('manualIngredient');
            const ingredient = input.value.trim();
            
            if (!ingredient) {
                alert('Please enter an ingredient name');
                return;
            }

            let list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
            if (!list.includes(ingredient)) {
                list.push(ingredient);
                localStorage.setItem('shoppingList', JSON.stringify(list));
                updateShoppingListCount();
                input.value = '';
                showShoppingList();
            } else {
                alert('This ingredient is already in your list');
            }
        }

        function updateShoppingListCount() {
            const list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
            document.getElementById('listCount').textContent = list.length;
        }

        function showShoppingList() {
            trackEvent('viewed_shopping_list');
            const list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
            const content = document.getElementById('shoppingListContent');
            
            if (list.length === 0) {
                content.innerHTML = '<div class="empty-state">Your shopping list is empty! Add ingredients from meals or manually below.</div>';
            } else {
                content.innerHTML = list.map((item, index) => `
                    <div class="shopping-list-item">
                        <span><strong>${item}</strong></span>
                        <button class="remove-btn" onclick="removeFromList(${index})">Remove</button>
                    </div>
                `).join('');
            }
            
            document.getElementById('shoppingListModal').style.display = 'block';
        }

        function removeFromList(index) {
            let list = JSON.parse(localStorage.getItem('shoppingList') || '[]');
            list.splice(index, 1);
            localStorage.setItem('shoppingList', JSON.stringify(list));
            updateShoppingListCount();
            showShoppingList();
        }

        function clearShoppingList() {
            if (confirm('Clear all items from shopping list?')) {
                localStorage.setItem('shoppingList', '[]');
                updateShoppingListCount();
                showShoppingList();
            }
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }

        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(html_code)

@app.route('/suggest')
def suggest():
    # Return 2 meals from each main category for a complete day plan
    breakfast_meals = [r for r in recipes if r['type'] == 'breakfast']
    lunch_meals = [r for r in recipes if r['type'] == 'lunch']
    dinner_meals = [r for r in recipes if r['type'] == 'dinner']
    
    result = {
        'breakfast': random.sample(breakfast_meals, min(2, len(breakfast_meals))),
        'lunch': random.sample(lunch_meals, min(2, len(lunch_meals))),
        'dinner': random.sample(dinner_meals, min(2, len(dinner_meals))),
        'all_meals': recipes
    }
    
    return jsonify(result)

@app.route('/all_recipes')
def all_recipes():
    return jsonify(recipes)

@app.route('/log_event')
def log_event():
    event = request.args.get('event', 'unknown')
    user_id = request.args.get('user_id', 'anonymous')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    log_entry = f"{timestamp} | User: {user_id} | Event: {event}\n"
    
    with open('logs/usage_log.txt', 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    return jsonify({'status': 'ok'})

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    feedback = data.get('feedback', '')
    rating = data.get('rating', 'not_provided')
    user_id = data.get('user_id', 'anonymous')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    feedback_entry = f"\n{'='*50}\n{timestamp} | User: {user_id}\nRating: {rating}\nFeedback: {feedback}\n{'='*50}\n"
    
    with open('logs/feedback.txt', 'a', encoding='utf-8') as f:
        f.write(feedback_entry)
    
    return jsonify({'status': 'success', 'message': 'Thank you for your feedback!'})

if __name__ == '__main__':
    app.run(debug=True)