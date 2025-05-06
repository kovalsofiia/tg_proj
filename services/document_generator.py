import logging
import os
from io import BytesIO
from docxtpl import DocxTemplate
from services.data_loader import DataLoader
try:
    from docx2pdf import convert
except ImportError:
    convert = None

class DocumentGenerator:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates_folder = os.path.normpath(os.path.join(current_dir, '..', 'templates'))
        self.loader = DataLoader()
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _build_context(self, fields, user_data):
        context = {}
        additional = user_data.get("additional_data", {})
        for field in fields:
            name = field['name']
            source = field.get('source', 'user_data')
            if source == 'system' and name == 'recipient':
                faculty = user_data.get('faculty', additional.get('faculty', ''))
                self.logger.debug(f"Processing recipient: faculty={faculty}")
                if not faculty:
                    self.logger.warning("Faculty not provided for recipient field")
                    value = ''
                else:
                    value = self.loader.get_dean(faculty)
                    if not value:
                        self.logger.warning(f"No dean found for faculty {faculty}")
                        value = 'No name for dean'
            else:
                value = user_data.get(name, additional.get(name, ""))
            context[name] = value
            self.logger.debug(f"Field {name}: value={value}")
        return context

    def generate(self, user_data, output_format='docx', return_bytes=False):
        document_type = user_data['document']
        template_info = self.loader.get_document_template(document_type)
        if not template_info:
            raise ValueError(f"Шаблон для типу документа '{document_type}' не знайдено.")
        template_path = os.path.join(self.templates_folder, template_info['template_file'])
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Файл шаблону '{template_path}' не знайдено.")
        fields = self.loader.get_document_fields(document_type)
        context = self._build_context(fields, user_data)
        doc = DocxTemplate(template_path)
        doc.render(context)
        full_name = user_data.get('full_name', 'unknown').replace(' ', '_')
        document_type_clean = document_type.replace(' ', '_')
        base_filename = f"{full_name}_{document_type_clean}"
        output_docx = f"{base_filename}.docx"
        doc.save(output_docx)
        self.logger.info(f"DOCX file saved: {output_docx}")
        if output_format.lower() == 'docx':
            if return_bytes:
                with open(output_docx, "rb") as f:
                    docx_bytes = BytesIO(f.read())
                os.remove(output_docx)
                return docx_bytes
            return output_docx
        if output_format.lower() == 'pdf':
            if convert is None:
                self.logger.error("docx2pdf не встановлено. Встановіть за допомогою 'pip install docx2pdf'.")
                os.remove(output_docx)
                raise RuntimeError("docx2pdf не встановлено. Встановіть за допомогою 'pip install docx2pdf'.")
            try:
                output_pdf = f"{base_filename}.pdf"
                convert(output_docx, output_pdf)
                self.logger.info(f"PDF file generated: {output_pdf}")
                if return_bytes:
                    with open(output_pdf, "rb") as f:
                        pdf_bytes = BytesIO(f.read())
                    os.remove(output_pdf)
                    os.remove(output_docx)
                    return pdf_bytes
                os.remove(output_docx)
                return output_pdf
            except Exception as e:
                self.logger.error(f"Помилка при конвертації в PDF: {str(e)}")
                os.remove(output_docx)
                raise RuntimeError(f"Помилка при генерації PDF: {str(e)}")