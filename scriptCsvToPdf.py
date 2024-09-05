# libraries used in the project
#!/usr/bin/env python3

import csv
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
import re

import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

def put_img_background(path, c):
    image_path = path
    image = ImageReader(image_path)
    largeur, hauteur = letter
    c.drawImage(image, 0, 0, width=largeur, height=hauteur)

# Extracting the numerical data of the price to sort
def convert_price(old_price):
    match = re.search(r'(\d+)\s*(.\d+)', old_price)
    if match:
        whole_part = match.group(1)
        decimal_part = match.group(2)
        decimal_part = decimal_part.rstrip("0").rstrip(".").rstrip(",").rstrip(" ")
        new_price = f"{whole_part}{decimal_part} €"
        return new_price
    match = re.search(r'(\d+)\s*(.\d+)', old_price)
    if match:
        whole_part = match.group(1)
        decimal_part = match.group(2)
        decimal_part = decimal_part.rstrip("0").rstrip(".").rstrip(",").rstrip(" ")
        new_price = f"{whole_part}{decimal_part} €"
        return new_price
    else:
        return old_price

def pdf_generation(filename, products_per_page):
    # Canvas creation and variable initialization
    c = canvas.Canvas(filename, pagesize=letter)
    y_position = 790
    old_color = "init"
    old_region = "init"
    old_subRegion = "init"
    police_ttf = "assets/Arial.ttf"  # path to the font
    police_ttf_subregion = "assets/Arial Bold.ttf"  # path to the font for subregion
    pdfmetrics.registerFont(TTFont('Arial', police_ttf))
    pdfmetrics.registerFont(TTFont('Arial Bold', police_ttf_subregion))
    # Generation of the front page of the pdf taking the background image with the centered logo and a description of 228Litres found on the website
    put_img_background("assets/FP_White.jpg", c)
    c.setFont("Arial", 50)
    c.drawString(170, 600, "Carte Des Vins")
    c.setFont("Arial", 12)
    c.drawString(75, 290, "Fruit d’un projet mené par trois amoureux du vin, 228 LITRES a ouvert ses portes fin")
    c.drawString(75, 273, "2018 dans le but de mettre en valeur les belles bouteilles découvertes par ses fondateurs.")
    c.drawString(75, 256,"Pierre, Louis et Robin s’activent en salle (mais aussi en boutique)  pour vous offrir la")
    c.drawString(75, 239,"meilleure expérience possible autour de nos vins. Notre équipe organise également de")
    c.drawString(75, 222,"nombreuses dégustations ou événements pour partager nos coups de cœur et notre passion.")
    c.drawString(75, 205,"N’hésitez pas à pousser pour demander conseil ou à nous contacter au sujet des différents")
    c.drawString(75, 188,"services que nous proposons.")
    c.drawString(75, 171,"Nos métiers comprennent le service du vin et la recherche des meilleurs accords à table, les")
    c.drawString(75, 154,"conseils pour une constitution de cave ou de carte de restaurant, ainsi que l’organisation")
    c.drawString(75, 137,"d’événements autour du vin et de dégustations thématiques ou sur-mesure")
    c.drawString(75, 120,"au sein de notre bar ou chez vous.")
    c.showPage()

    # Font we use in the pdf (same as 228Litres Website)
    c.setFont("Arial", 18)
    # Looping for each page we generate
    Sakés = 0
    beer = 0
    Magnum = 0
    CidresPoirés = 0
    Vin = 0
    VinB = 0
    VinMa = 0
    VinRos = 0
    VinRou = 0
    champagne = 0
    autrebull = 0
    old_cat = ""
    for products in products_per_page:
        typeOfProduct = products["Catégorie"]
        color = products["Couleur"]
        if color == "Orange":
            color = "Vin de macération"
        region = products["Région (Vin)"]
        subRegion = products["Note Interne Produit"]
        cat = products["Catégorie"]
        if products["Pays"] != "France":
            subRegion = region
            region = products["Pays"]
        if products["Catégorie"] == "Champagne > Effervescent":
            tmp = color
            color = region
            region = tmp
        elif products["Contenance"] == "1,5 L":
            color = "Vin " + color
        if "Champagne" in old_color and old_color != color and products["Contenance"] == "1,5 L":
            y_position = 790
            c.showPage()
        if products["Catégorie"] == "Sakés":
            old_color = color
        if "Bières" in cat:
            cat = "Bières"
        # checking if we have to change page, if to low on the image (y_position < 50 OR region != old_region OR color != old_color)
        if y_position < 50 or (cat != old_cat and (cat == "Sakés" or "Bières" == cat or cat == "Cidres & Poirés")):
            y_position = 790
            c.showPage()
        if Magnum == 0 and products["Contenance"] == "1,5 L":
            if y_position != 790:
                c.showPage()
            put_img_background("assets/FP_White.jpg", c)
            largeur_texte = c.stringWidth("Magnums", "Arial", 50)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 50)
            c.drawString(X, 600, "Magnums")
            c.showPage()
            y_position = 790
            Magnum = 1
        if champagne == 0:
            if y_position != 790:
                c.showPage()
            put_img_background("assets/FP_White.jpg", c)
            largeur_texte = c.stringWidth("Bulles et Champagne", "Arial", 50)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 50)
            c.drawString(X, 600, "Bulles et Champagne")
            c.showPage()
            y_position = 790
            champagne = 1
        if VinB == 0 and "Effervescent" != products["Type de vin"] and "Champagne > Effervescent" != products["Catégorie"]:
            if y_position != 790:
                c.showPage()
            put_img_background("assets/FP_White.jpg", c)
            largeur_texte = c.stringWidth("Blancs", "Arial", 50)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 50)
            c.drawString(X, 600, "Blancs")
            c.showPage()
            y_position = 790
            VinB = 1
        if VinMa == 0 and old_color != color and color == "Vin de macération":
            if y_position != 790:
                c.showPage()
            put_img_background("assets/FP_White.jpg", c)
            largeur_texte = c.stringWidth("Macérations", "Arial", 50)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 50)
            c.drawString(X, 600, "Macérations")
            c.showPage()
            y_position = 790
            VinMa = 1
        if VinRos == 0 and color == "Rosé" and "Effervescent" != products["Type de vin"]:
            if y_position != 790:
                c.showPage()
            put_img_background("assets/FP_White.jpg", c)
            largeur_texte = c.stringWidth("Rosés", "Arial", 50)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 50)
            c.drawString(X, 600, "Rosés")
            c.showPage()
            y_position = 790
            VinRos = 1
        if VinRou == 0 and color == "Rouge" and "Effervescent" != products["Type de vin"]:
            if y_position != 790:
                c.showPage()
            put_img_background("assets/FP_White.jpg", c)
            largeur_texte = c.stringWidth("Rouges", "Arial", 50)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 50)
            c.drawString(X, 600, "Rouges")
            c.showPage()
            y_position = 790
            VinRou = 1
        if CidresPoirés == 0 and "Cidres & Poirés" == products["Catégorie"]:
            if y_position != 790:
                c.showPage()
            put_img_background("assets/FP_White.jpg", c)
            largeur_texte = c.stringWidth("Cidres & Poirés", "Arial", 50)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 50)
            c.drawString(X, 600, "Cidres & Poirés")
            c.showPage()
            y_position = 790
            CidresPoirés = 1
        if Sakés == 0 and "Sakés" == products["Catégorie"]:
            if y_position != 790:
                c.showPage()
            put_img_background("assets/FP_White.jpg", c)
            largeur_texte = c.stringWidth("Sakés", "Arial", 50)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 50)
            c.drawString(X, 600, "Sakés")
            c.showPage()
            y_position = 790
            Sakés = 1
        if beer == 0 and "Bières" in products["Catégorie"]:
            if y_position != 790:
                c.showPage()
            put_img_background("assets/FP_White.jpg", c)
            largeur_texte = c.stringWidth("Bière", "Arial", 50)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 50)
            c.drawString(X, 600, "Bières")
            c.showPage()
            y_position = 790
            beer = 1
        if CidresPoirés == 0 and "Cidres & Poirés" == products["Catégorie"]:
            largeur_texte = c.stringWidth("Cidres & Poirés", "Arial", 36)
            X = 300 - (largeur_texte / 2)
            c.setFont("Arial", 36)
            y_position -= 50
            c.drawString(X, y_position, "Cidres & Poirés")
            CidresPoirés = 1
        if Sakés == 0 and "Sakés" == products["Catégorie"]:
            largeur_texte = c.stringWidth("Sakés", "Arial", 36)
            X = 300 - (largeur_texte / 2)
            y_position -= 50
            c.setFont("Arial", 36)
            c.drawString(X, y_position, "Sakés")
            Sakés = 1
        if beer == 0 and "Bières" in products["Catégorie"]:
            largeur_texte = c.stringWidth("Bières", "Arial", 36)
            X = 300 - (largeur_texte / 2)
            y_position -= 50
            c.setFont("Arial", 36)
            c.drawString(X, y_position, "Bières")
            beer = 1
        if old_color != color or y_position == 790 or old_region != region:
            old_subRegion = ""
            if y_position <= 150:
                c.showPage()
                y_position = 790
                c.setFont("Arial", 36)
                y_position -= 50
                # centering color
                if "Bières" in products["Catégorie"]:
                    y_position = y_position
                elif color != old_color and ("Effervescent" == products["Type de vin"] or products["Contenance"] == "1,5 L"):
                    largeur_texte = c.stringWidth(color, "Arial", 36)
                    X = 300 - (largeur_texte / 2)
                    c.drawString(X, y_position, f"{color}")
                    y_position -= 50
                # centering region according to the size of the text
                largeur_texte = c.stringWidth(region, "Arial", 27)
                X = 300 - (largeur_texte / 2)
                c.setFont("Arial", 27)
                c.drawString(X, y_position, f"{region}")
                y_position -= 35
            else:
                c.setFont("Arial", 36)
                # centering color
                y_position -= 50
                if "Bières" in products["Catégorie"]:
                    y_position = y_position
                elif color != old_color and ( "Effervescent" == products["Type de vin"] or products["Contenance"] == "1,5 L"):
                    largeur_texte = c.stringWidth(color, "Arial", 36)
                    X = 300 - (largeur_texte / 2)
                    c.drawString(X, y_position, f"{color}")
                    y_position -= 50
                # centering region according to the size of the text
                largeur_texte = c.stringWidth(region, "Arial", 27)
                X = 300 - (largeur_texte / 2)
                c.setFont("Arial", 27)
                c.drawString(X, y_position, f"{region}")
                y_position -= 35
        old_color = color
        old_region = region
        old_cat = cat
        if old_subRegion != subRegion and subRegion != region and products["Catégorie"] != "Sakés" and products["Catégorie"] != "Cidres & Poirés" and typeOfProduct != "Bières":
            y_position -= 15
            c.setFont("Arial Bold", 15)
            c.drawString(75, y_position, subRegion)
            y_position -= 20
        old_subRegion = subRegion
        nom = products["Nom du produit"]
        producer = products["Producteur"]
        if products["Année"]:
            year = products["Année"]
        else:
            year = "NM"
        volume = products["Contenance"]
        if volume == "0,75 L":
            volume = ""
        price_ATI = products["Tarif Bar TTC"]
        # Writing the wine informations on the PDF
        c.setFont("Arial", 10)
        c.drawString(75, y_position, year)
        c.drawString(490, y_position, volume)
        c.drawRightString(550, y_position, f"{price_ATI}")
        c.setFont("Arial", 10)
        name_width = c.stringWidth(nom, "Arial", 10)
        producer_width = c.stringWidth(producer, "Arial", 10)
        if name_width > 150 or producer_width > 150:
            if name_width > 150:
                name_delimiteur_index = nom.rfind(' ', 0, 35)
            else:
                name_delimiteur_index = -1
            if producer_width > 150:
                producer_delimiteur_index = producer.rfind(' ', 0, 35)
            else:
                producer_delimiteur_index = -1
            if name_delimiteur_index != -1 or producer_delimiteur_index != -1:
                name_row1 = nom[:name_delimiteur_index]
                name_row2 = nom[name_delimiteur_index + 1:]
                producer_row1 = producer[:producer_delimiteur_index]
                producer_row2 = producer[producer_delimiteur_index + 1:]
                if name_delimiteur_index != -1:
                    c.drawString(115, y_position, name_row1)
                else:
                    c.drawString(115, y_position, nom)
                c.setFont("Arial", 10)
                if producer_delimiteur_index != -1:
                    c.drawString(310, y_position, producer_row1)
                else:
                    c.drawString(310, y_position, producer)
                y_position -= 14
                c.setFont("Arial", 10)
                if name_delimiteur_index != -1:
                    c.drawString(115, y_position, name_row2)
                c.setFont("Arial", 10)
                if producer_delimiteur_index != -1:
                    c.drawString(310, y_position, producer_row2)
        else:
            c.drawString(115, y_position, f"{nom}")
            c.drawString(310, y_position, producer)
        c.setFont("Arial", 10)
        # newline for a new product
        y_position -= 15
    c.save()

def convert_price_to_int(price_str):
    numeric_chars = [char for char in price_str if char.isdigit()]
    numeric_str = ''.join(numeric_chars)
    price_int = int(numeric_str)
    return price_int

def sort_by_cheapest(lst):
    new_list = []
    prod = ""
    exclude_prod = []
    min = sys.maxsize
    while len(lst) != len(new_list):
        for product in lst:
            if min > convert_price_to_int(product["Tarif Bar TTC"].replace('\u202F', '')) and product["Producteur"] + product["Note Interne Produit"] not in exclude_prod:
                min = convert_price_to_int(product["Tarif Bar TTC"].replace('\u202F', ''))
                prod = product["Producteur"] + product["Note Interne Produit"]
        for product in lst:
            if product["Producteur"] + product["Note Interne Produit"] == prod:
                new_list.append(product)
        exclude_prod.append(prod)
        min = sys.maxsize
    return new_list

# creation of the window
root = tk.Tk()
root.withdraw()
data = ""
# Ask for the user input
data = simpledialog.askstring("Input", "Enter your database filename")
filename_pdf = simpledialog.askstring("Input", "Enter your filename")
filename_pdf += ".pdf"
try:
    if not data:
        messagebox.showinfo("Status",f"Canceled")
        sys.exit()
    with open(data + ".csv", 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
except IOError:
    messagebox.showinfo("Status",f"Le fichier '{data}.csv' n'existe pas.")
    sys.exit()

# csv to dictionary and start to remove all product that aren't wine
list_product_red = []
list_product_white = []
list_product_pink = []
list_product_bul = []
list_product_orange = []
list_product_mag_red = []
list_product_mag_white = []
list_product_mag_pink = []
list_product_mag_bul = []
list_product_mag_orange = []
list_product_mag_otherbub = []
list_product_cidre = []
list_product_sak = []
list_product_beer = []
list_product_otherbub = []
with open(data + ".csv", 'r', newline='\n', encoding='utf-8') as file:
    file.readline()
    # skip first line that isnt being used
    csv_reader = csv.DictReader(file, delimiter=';')
    for row in csv_reader:
        product = {
                "Type de produit" : row["Type de produit"],
                "Nom du produit" : row["Nom du produit"],
                "Nom de la variante" : row["Nom de la variante"],
                "Quantité théorique" : int(row["Quantité théorique"]),
                "Note interne" : row["Note interne"],
                "Région (Vin)" : row["Région (Vin)"],
                "Catégorie" : row["Catégorie"],
                "Pays" : row["Pays"],
                "Producteur" : row["Producteur"],
                "Année" : row["Millésime (Vin & Spititueux)"],
                "Contenance" : row["Contenance"],
                "Couleur" : row["Couleur (Vin & Bière)"],
                "Tarif Bar TTC" : convert_price(row["Tarif Bar TTC"].replace('\u202F', '')),
                "Boutique" : row["Boutique"],
                "Type de vin" : row["Type de vin"],
                "Note Interne Produit" : row["Note Interne Produit"],
                "Note de dégustation" : row["Note de dégustation"]
        }
        if product["Boutique"] == "228 LITRES" and product["Quantité théorique"] > 0 and product["Note interne"] != "Non" and product ["Note de dégustation"] != "Non":
            if product["Type de produit"] == "Vin":
                if product["Contenance"] == "1,5 L":
                    if "Effervescent" in product["Catégorie"]:
                        list_product_mag_bul.append(product)
                    elif "Effervescent" in product["Type de vin"]:
                        list_product_mag_otherbub.append(product)
                    elif "Rouge" in product["Couleur"]:
                        list_product_mag_red.append(product)
                    elif "Blanc" in product["Couleur"]:
                        list_product_mag_white.append(product)
                    elif "Rosé" in product["Couleur"]:
                        list_product_mag_pink.append(product)
                    elif "Orange" in product["Couleur"]:
                        list_product_mag_orange.append(product)
                elif product["Catégorie"] == "Sakés":
                    list_product_sak.append(product)
                elif product["Catégorie"] == "Cidres & Poirés":
                    list_product_cidre.append(product)
                else:
                    if "Effervescent" in product["Catégorie"]:
                        list_product_bul.append(product)
                    elif "Bières" in product["Catégorie"]:
                        list_product_beer.append(product)
                    elif "Effervescent" in product["Type de vin"]:
                        list_product_otherbub.append(product)
                    elif "Rouge" in product["Couleur"]:
                        list_product_red.append(product)
                    elif "Blanc" in product["Couleur"]:
                        list_product_white.append(product)
                    elif "Rosé" in product["Couleur"]:
                        list_product_pink.append(product)
                    elif "Orange" in product["Couleur"]:
                        list_product_orange.append(product)

def extract_price(product):
    price = product["Tarif Bar TTC"].replace('\u202F', '')
    match = re.search(r'\d+', price)
    if match:
        return int(match.group())
    else:
        return 0


# Sort all Dictionary
list_product_bul = sorted(list_product_bul, key=lambda x: (extract_price(x)))
list_product_bul = sort_by_cheapest(list_product_bul)
list_product_otherbub = sorted(list_product_otherbub, key=lambda x: (extract_price(x)))
list_product_otherbub = sort_by_cheapest(list_product_otherbub)
list_product_white = sorted(list_product_white, key=lambda x: (extract_price(x)))
list_product_white = sort_by_cheapest(list_product_white)
list_product_orange = sorted(list_product_orange, key=lambda x: (extract_price(x)))
list_product_orange = sort_by_cheapest(list_product_orange)
list_product_pink = sorted(list_product_pink, key=lambda x: (extract_price(x)))
list_product_pink = sort_by_cheapest(list_product_pink)
list_product_red = sorted(list_product_red, key=lambda x: (extract_price(x)))
list_product_red = sort_by_cheapest(list_product_red)
list_product_mag_bul = sorted(list_product_mag_bul, key=lambda x: (extract_price(x)))
list_product_mag_bul = sort_by_cheapest(list_product_mag_bul)
list_product_mag_otherbub = sorted(list_product_mag_otherbub, key=lambda x: (extract_price(x)))
list_product_mag_otherbub = sort_by_cheapest(list_product_mag_otherbub)
list_product_mag_white = sorted(list_product_mag_white, key=lambda x: (extract_price(x)))
list_product_mag_white = sort_by_cheapest(list_product_mag_white)
list_product_mag_orange = sorted(list_product_mag_orange, key=lambda x: (extract_price(x)))
list_product_mag_orange = sort_by_cheapest(list_product_mag_orange)
list_product_mag_pink = sorted(list_product_mag_pink, key=lambda x: (extract_price(x)))
list_product_mag_pink = sort_by_cheapest(list_product_mag_pink)
list_product_mag_red = sorted(list_product_mag_red, key=lambda x: (extract_price(x)))
list_product_mag_red = sort_by_cheapest(list_product_mag_red)
list_product_cidre = sorted(list_product_cidre, key=lambda x: (extract_price(x)))
list_product_cidre = sort_by_cheapest(list_product_cidre)
list_product_sak = sorted(list_product_sak, key=lambda x: (extract_price(x)))
list_product_sak = sort_by_cheapest(list_product_sak)
list_product_beer = sorted(list_product_beer, key=lambda x: (extract_price(x)))
list_product_beer = sort_by_cheapest(list_product_beer)
list_product_sort_bul = sorted(list_product_bul, key=lambda x: (x["Couleur"],x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_otherbub = sorted(list_product_otherbub, key=lambda x: (x["Couleur"],x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_white = sorted(list_product_white, key=lambda x: (x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_orange = sorted(list_product_orange, key=lambda x: (x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_pink = sorted(list_product_pink, key=lambda x: (x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_red = sorted(list_product_red, key=lambda x: (x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_mag_bul = sorted(list_product_mag_bul, key=lambda x: (x["Couleur"],x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_mag_otherbub = sorted(list_product_mag_otherbub, key=lambda x: (x["Couleur"],x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_mag_white = sorted(list_product_mag_white, key=lambda x: (x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_mag_orange = sorted(list_product_mag_orange, key=lambda x: (x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_mag_pink = sorted(list_product_mag_pink, key=lambda x: (x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_mag_red = sorted(list_product_mag_red, key=lambda x: (x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_cidre = sorted(list_product_cidre, key=lambda x: (x["Couleur"],x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_sak = sorted(list_product_sak, key=lambda x: (x["Couleur"],x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))
list_product_sort_beer = sorted(list_product_beer, key=lambda x: (x["Couleur"],x["Pays"] != "France",x["Pays"],x["Région (Vin)"],x["Note Interne Produit"]))



# Creation of the final list of dictionaries
final_list_product_sorted = (list_product_sort_bul)
final_list_product_sorted.extend(list_product_sort_otherbub)
final_list_product_sorted.extend(list_product_sort_white)
final_list_product_sorted.extend(list_product_sort_orange)
final_list_product_sorted.extend(list_product_sort_pink)
final_list_product_sorted.extend(list_product_sort_red)
final_list_product_sorted.extend(list_product_sort_mag_bul)
final_list_product_sorted.extend(list_product_sort_mag_otherbub)
final_list_product_sorted.extend(list_product_sort_mag_white)
final_list_product_sorted.extend(list_product_sort_mag_orange)
final_list_product_sorted.extend(list_product_sort_mag_pink)
final_list_product_sorted.extend(list_product_sort_mag_red)
final_list_product_sorted.extend(list_product_sort_cidre)
final_list_product_sorted.extend(list_product_sort_sak)
final_list_product_sorted.extend(list_product_sort_beer)




pdf_generation(filename_pdf, final_list_product_sorted)
# pdf_generation(filename_pdf, final_product_list_sorted)
messagebox.showinfo("Status",f"The file '{filename_pdf}' has been created. Might Dionysos be with you!")