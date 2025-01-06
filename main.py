import json
from openai import OpenAI
import re

client = OpenAI()

class ProductEnhancer:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    
    # def string_to_json(self, data_string):
    #     """Converts a string with key-value pairs to a JSON string."""
    #     data_dict = {}
    #     lines = re.split(r', ', data_string.strip())
    #     for line in lines:
    #         key, value = line.split(':', 1)
    #         data_dict[key.strip()] = value.strip().strip('"') 
            
    #     return data_dict
    
    def enhance_product_data(self):
        """Enhance product data using OpenAI API."""
        with open(self.input_file, "r") as f:
            products = json.load(f)

        enhanced_data = []

        for product in products:
            try:
                prompt = (
                    # f"Product Name: {product['name']},"
                    # f"Price: {product['price']},"
                    # f"Rating: {product['rating']},"
                    # f"Description: {product['description']},"
                    
                    # "Categorize this product from Beauty, Health, Grocery , Books, Car, Motorbike, Industrial, Home, Kitchen, Pets, Men's Fashion , Mobiles, Computers , Movies, Music & Video Games , Sports, Fitness, Bags, Luggage, Toys, Baby Products, Kids' Fashion , TV, Appliances, Electronics , The name of this section should be Category,"
                    # "infer its pricing segment (budget, mid-market, premium), the name of this section should be Pricing Segment,"
                    # "and create a catchy tagline, the name of this section should be Tagline, and don't add \ , ** or numbers anywhere,"
                    # "For example JSON output should be in following format - "
                    # '{"Category": "Electronics", "Pricing Segment": "Mid-market", "Tagline": "The best in class electronics"}'
                    f"Product Name: {product['name']}\n"
                    f"Price: {product['price']}\n"
                    f"Rating: {product['rating']}\n\n"
                    "Enhance the product information."
                )
                
                functions = [
                    {
                        "name": "enhance_product",
                        "description": "Categorize the product, infer its pricing segment, and create a catchy tagline.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "Category": {
                                    "type": "string",
                                    "description": "The category of the product.Categorize this product from Beauty, Health, Grocery , Books, Car, Motorbike, Industrial, Home, Kitchen, Pets, Men's Fashion , Mobiles, Computers , Movies, Music & Video Games , Sports, Fitness, Bags, Luggage, Toys, Baby Products, Kids, Fashion , TV, Appliances, Electronics",
                                },
                                "Pricing Segment": {
                                    "type": "string",
                                    "description": "The pricing segment of the product (e.g., budget, mid-market, premium).",
                                },
                                "Tagline": {
                                    "type": "string",
                                    "description": "A catchy tagline for the product.",
                                },
                            },
                            "required": ["Category", "Pricing Segment", "Tagline"],
                        },
                    }
                ]

                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    functions=functions
                )

                
                assistant_message = completion.choices[0].message
                # print("Function Call: ",assistant_message.function_call)
                # print()
                # print("Assistant message: ",assistant_message)
                # structured_response = json.loads(assistant_message) 
                
                if assistant_message.function_call:
                    function_name = assistant_message.function_call.name
                    # print(f"Function {function_name} called.")
                    arguments = json.loads(assistant_message.function_call.arguments)
                
                enhanced_data.append({
                    "product": product,
                    "enhanced_data": arguments
                })
                
                print(f"Enhanced data for {product['name']} saved.")

            except Exception as e:
                print(f"Error processing product {product['name']}: {e}")

        with open(self.output_file, "w") as f:
            json.dump(enhanced_data, f, indent=4)
    
    
if __name__ == "__main__":
    input_file = "output/scraped_data.json"
    output_file = "output/enhanced_data.json"

    enhancer = ProductEnhancer(input_file, output_file)
    enhancer.enhance_product_data()


