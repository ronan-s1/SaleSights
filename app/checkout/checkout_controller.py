# checkout_processing.py
import cv2
import pyzbar.pyzbar as pyzbar
from checkout.product_fetch_data import fetch_products, get_product_by_barcode

def get_products():
    products = fetch_products()
    return list(products)


def process_frame(frame, session_state):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Scan the frame for barcodes
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        barcode_data = obj.data.decode("utf-8")

        # Only process the barcode if it's not already processed
        if barcode_data not in session_state:
            session_state[barcode_data] = True
            return {
                "barcode_data": barcode_data,
                "rectangle_coords": (
                    obj.rect.left,
                    obj.rect.top,
                    obj.rect.left + obj.rect.width,
                    obj.rect.top + obj.rect.height,
                ),
            }


def process_decoded_barcode(data):
    barcode_data = data["barcode_data"]
    product = get_product_by_barcode(barcode_data)
    
    if product:
        return product
    
    return f"No product with scanned barcode {barcode_data}."
    
    
    
    

    