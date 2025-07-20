# import pdfkit

# config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

# def generate_certificate_pdf(certificate_type: str, data: dict, output_path: str):
#     template_path = f"templates/{certificate_type.lower()}_template.html"

#     with open(template_path, "r") as f:
#         html_template = f.read()

#     html_filled = html_template.format(**data)

#     pdfkit.from_string(html_filled, output_path, configuration=config)
import pdfkit
from jinja2 import Environment, FileSystemLoader

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader("templates"))

def generate_certificate_pdf(certificate_type: str, data: dict, output_path: str):
    template = env.get_template(f"{certificate_type.lower()}_template.html")
    html_filled = template.render(data)
    pdfkit.from_string(html_filled, output_path, configuration=config)
