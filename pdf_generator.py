from fpdf import FPDF
import pandas as pd
import glob
import argparse
import os
import shutil

def get_photo_num(image_name):
    try: 
        return int(image_name.split("_")[-1].split(".")[0])
    except:
        print("Image number could not be found for - ", image_name)
        pass
    
def create_new_pdf():
    pdf=PDF( )
    pdf.alias_nb_pages()
    # Add new page. Without this you cannot create the document.
    pdf.add_page()

    # Page header

    pdf.ln(0.25)

    # Smaller font for image captions
    pdf.set_font('Arial','B',10.0)
    return pdf


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


def main(csv_file, photo_dir, output_dir ):


    if os.path.exists(output_dir ):
        shutil.rmtree(output_dir )
    os.makedirs(output_dir )

    df = pd.read_csv(csv_file)
    lookup_dict = df.set_index('Photo #').to_dict()

    # Import glob module to find all the files matching a pattern

    # Image extensions
    #image_extensions = [  + "/*.jpg"]
    
    # This list will hold the images file names
    images = []


    #for extension in image_extensions:
    images.extend(glob.glob(photo_dir + "/*.jpg" ))
    

    pdf = create_new_pdf()


    i = 0 
    for image in images:
        i+=1
        image_num = get_photo_num(image)
        if image_num in  lookup_dict['Description of Property']:
            desc = lookup_dict['Description of Property'][image_num]
            desc = str(desc).encode('latin-1', 'replace').decode('latin-1')
            value = lookup_dict['Value'][image_num]
            location =  lookup_dict['Location'][image_num]
        else:
            desc = 'Description of Property is missing'
            value = "value is missing"
            location = "location is missing"
            

        pdf.image(image, w=pdf.w/2.0, h=pdf.h/4.0)
        
        pdf.ln(10)
        
        pdf.cell(90)

        pdf.ln(.5)
        pdf.cell(0, 10, "Image Path:  " + str(image), 0, 1)

        pdf.cell(50)
        pdf.ln(.5)
        pdf.cell(0, 10, "Value:  $" + str(value) , 0, 1)

        pdf.cell(50)
        pdf.ln(.5)
        pdf.cell(0, 10, "Description: " + str(desc) , 0, 1)
        

        pdf.cell(50)
        pdf.ln(.5)
        pdf.cell(0, 10, "Location: " + str(location), 0, 1)

        #pdf.cell(10)
        pdf.ln(10)
        if (i % 2) == 0 :
            pdf.output( output_dir + '/images-in-folder' + str(int(i/2)) +  '.pdf','F')
            pdf = create_new_pdf()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_csv')
    parser.add_argument('photo_dir')
    parser.add_argument('output_dir')
    args = parser.parse_args()

    #python pdf_generator.py 'inventory.csv'  "Photos\DTR Mallory Inventory"  "output"
    main(args.input_csv, args.photo_dir , args.output_dir )


