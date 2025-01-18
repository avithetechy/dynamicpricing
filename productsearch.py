import google.generativeai as genai

GOOGLE_API_KEY="AIzaSyClP0lYfgl9G3LTxkvL8ViRVQ_hNj4ddyo"

url = "https://www.amazon.in/Samsung-Awesome-Iceblue-Storage-Nightography/dp/B0CWPDYS2C/ref=sr_1_3?crid=2BWPLUDSIWAQ3&dib=eyJ2IjoiMSJ9.gvLy-PYJinh9bzFCyaBbwTCmz1SA70B5lbNEHXmMSIkdVYOPdG9VDwrFtRid2z9hwfNyt6nerV_-x83ezqCQtXSxzRXthLdfQxZvY8sPZjP6zoUcy9d7Jgx0ZcfIIxWybiojqwYC8ryB7Z_zD99k5ykT0lCGMHj2FDPsMq2m9aaIRtCOIpy4A7yvbxGuf-O0T7B__Q-U77cpDMHCP_DHMOz3iWBpN6J2_UfQj8lcKCw.HfSPLZlpSgScb_ZQelV9Efd7c00S8zB01Trynfc3XeY&dib_tag=se&keywords=samsung%2Ba35%2B5g&nsdOptOutParam=true&qid=1736304439&sprefix=%2Caps%2C508&sr=8-3&th=1"

text_sys_prompt = f"extract only the product name like(Samsung Galaxy A35 5G (Awesome Iceblue, 8GB RAM, 128GB Storage) | Premium Glass Back | 50 MP Main Camera (OIS) | Nightography | IP67 | Corning Gorilla Glass Victus+ | sAMOLED with Vision Booster) and its price like (₹24,999) from this url:{url}"

genai.configure(api_key=GOOGLE_API_KEY)
#model1 = genai.GenerativeModel(model='gemini-1.5-pro',system_instruction='text_sys_prompt')
model2 = genai.GenerativeModel('gemini-1.5-flash')
response = model2.generate_content(text_sys_prompt)
reslst = []
if response.candidates:  # Check if there are any candidates
    first_candidate = response.candidates[0] # Get the first candidate
    if first_candidate.content and first_candidate.content.parts: #Check if content and parts exist
        text_output = first_candidate.content.parts[0].text

        # Now, extract name and price from the text output
        lines = text_output.strip().split('\n') #Splitting the output into lines
        product_name = None
        price = None
        for line in lines:
            if "Product Name:" in line:
                product_name = line.split("Product Name:")[1].strip()
            elif "Price:" in line:
                price = line.split("Price:")[1].strip()
        if product_name:
            reslst.append(product_name) 
        if price:
            reslst.append(price) 
    else:
        print("No content or parts found in the response.")

else:
    print("No candidates found in the response.")

flipkart_url = "https://www.flipkart.com/samsung-galaxy-a35-5g-awesome-iceblue-128-gb/p/itm9684d2fe9201e?pid=MOBGYT2HEYWFCG8Q&lid=LSTMOBGYT2HEYWFCG8QSW6D6Y&marketplace=FLIPKART&q=samsung+a35+5g&store=tyy%2F4io&srno=s_1_6&otracker=search&otracker1=search&fm=organic&iid=24e89b53-e9be-4e16-9f5f-56b628afab79.MOBGYT2HEYWFCG8Q.SEARCH&ppt=hp&ppn=homepage&ssid=x10vwgkgzk0000001736318580377&qH=964f4f9ee93888b2"

text_sys_prompt2 = f"extract only the product name like(Samsung Galaxy A35 5G (Awesome Iceblue, 8GB RAM, 128GB Storage) | Premium Glass Back | 50 MP Main Camera (OIS) | Nightography | IP67 | Corning Gorilla Glass Victus+ | sAMOLED with Vision Booster) and its price like (₹30,999) from this url:{flipkart_url}"

#genai.configure(api_key=GOOGLE_API_KEY)
#model1 = genai.GenerativeModel(model='gemini-1.5-pro',system_instruction='text_sys_prompt')
#model2 = genai.GenerativeModel('gemini-1.5-flash')
response2 = model2.generate_content(text_sys_prompt2)

if response2.candidates:  # Check if there are any candidates
    first_candidate = response2.candidates[0] # Get the first candidate
    if first_candidate.content and first_candidate.content.parts: #Check if content and parts exist
        text_output = first_candidate.content.parts[0].text

        # Now, extract name and price from the text output
        lines = text_output.strip().split('\n') #Splitting the output into lines
        product_name = None
        price = None
        for line in lines:
            if "Product Name:" in line:
                product_name = line.split("Product Name:")[1].strip()
            elif "Price:" in line:
                price = line.split("Price:")[1].strip()
        if product_name:
            reslst.append(product_name)
        if price:
            reslst.append(price)
    else:
        print("No content or parts found in the response.")

else:
    print("No candidates found in the response.")

print(reslst)